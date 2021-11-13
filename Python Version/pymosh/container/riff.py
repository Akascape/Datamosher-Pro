import os
import struct
from io import IOBase

list_headers = (b'RIFF', b'LIST')


class UnexpectedEOF(Exception):
    pass


class RiffIndexChunk(object):
    def __init__(self, fh, header, length, position):
        self.file = fh
        self.header = header
        self.length = int(length)
        self.position = position

    def __str__(self):
        return str(self.bytes())

    def bytes(self) -> bytes:
        return self.header + struct.pack('<I', self.length) + self.data

    def __len__(self):
        return self.length

    def __getslice__(self, start, end):
        if start is None:
            start = 0
        if end is None:
            end = self.length

        current = self.file.tell()
        self.file.seek(self.position+start)
        if start < end and start <= self.length:
            if end > self.length:
                end = self.length
            data = self.file.read(end-start)
            self.file.seek(current)
            return data
        else:
            return ''

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.__getslice__(index.start, index.stop)
        return self[index:index+1]

    def _data(self):
        """Read data from the file."""
        current_position = self.file.tell()
        self.file.seek(self.position)
        data = self.file.read(self.length)
        self.file.seek(current_position)
        if self.length % 2:
            data += b'\x00'  # Padding byte
        return data
    data = property(_data)

    def as_data(self):
        """Return a RiffDataChunk read from the file."""
        raise NotImplementedError()


class RiffIndexList(RiffIndexChunk):
    def __init__(self, header, list_type, *args, **kwargs):
        self.header = header
        self.type = list_type
        self.file = kwargs.get('file', None)
        self.position = kwargs.get('position', 0)
        self.chunks = kwargs.get('chunks', [])

    def __getitem__(self, index):
        return self.chunks[index]

    def __setitem__(self, index, value):
        return self.chunks.__setitem__(index, value)

    def __delitem__(self, index):
        return self.chunks.__delitem__(index)

    def __iter__(self):
        return iter(self.chunks)

    def __len__(self):
        """Return total data length of the list and its headers."""
        return self.chunk_length() + len(self.type) + len(self.header) + 4

    def chunk_length(self):
        length = 0
        for chunk in self.chunks:
            chunk_len = len(chunk)
            length += chunk_len + 8  # Header and length bytes
            length += chunk_len % 2  # Pad byte
        return length

    def __str__(self):
        return str(self.bytes())

    def bytes(self) -> bytes:
        """Returns a byte representation of the chunk."""
        length_bytes = struct.pack('<I', self.chunk_length() + len(self.type))
        return self.header + length_bytes + self.type

    class NotFound(Exception):
        """Indicates a chunk or list was not found by the find method."""
        pass

    def find(self, header, list_type=None):
        """Find the first chunk with specified header and optional list type."""
        for chunk in self:
            if chunk.header == header and (list_type is None or (header in
                                                                 list_headers and chunk.type == list_type)):
                return chunk
            elif chunk.header in list_headers:
                try:
                    result = chunk.find(header, list_type)
                    return result
                except chunk.NotFound:
                    pass
        if list_type is None:
            raise self.NotFound('Chunk \'{0}\' not found.'.format(header))
        else:
            raise self.NotFound('List \'{0} {1}\' not found.'.format(header,
                                                                     list_type))

    def find_all(self, header, list_type=None):
        """Find all direct children with header and optional list type."""
        found = []
        for chunk in self:
            if chunk.header == header and (not list_type or (header in
                                                             list_headers and chunk.type == list_type)):
                found.append(chunk)
        return found

    def replace(self, child, replacement):
        """Replace a child chunk with something else."""
        for i in range(len(self.chunks)):
            if self.chunks[i] == child:
                self.chunks[i] = replacement

    def remove(self, child):
        """Remove a child element."""
        for i in range(len(self)):
            if self[i] == child:
                del self[i]


class RiffDataChunk(object):
    """A RIFF chunk with data in memory instead of a file."""

    def __init__(self, header, data):
        self.header = header
        self.length = len(data)
        self.data = data

    @staticmethod
    def from_data(data):
        """Create a chunk from data including header and length bytes."""
        header, _ = struct.unpack('4s<I', data[:8])
        data = data[8:]
        return RiffDataChunk(header, data)

    def bytes(self) -> bytes:
        """Returns a byte array representation of the chunk."""
        return self.header + struct.pack('<I', self.length) + self.data

    def __str__(self):
        return str(self.bytes())

    def __len__(self):
        return self.length

    def __getslice__(self, start, end):
        return self.data[start:end]

    def __getitem__(self, index):
        return self.data[index]


class RiffIndex(RiffIndexList):
    def __init__(self):
        self.file = None
        self.chunks = []

    @staticmethod
    def from_file(filename: str):
        instance = RiffIndex()

        instance.file = open(filename, 'rb')
        instance.size = instance.get_size()
        instance.scan_file()

        return instance

    def write(self, fh: IOBase) -> None:
        def print_chunks(chunks):
            for chunk in chunks:
                fh.write(chunk.bytes())
                if chunk.header in (b'RIFF', b'LIST'):
                    print_chunks(chunk.chunks)

        print_chunks(self.chunks)

    def get_size(self):
        current = self.file.tell()
        self.file.seek(0, 2)
        size = self.file.tell()
        self.file.seek(current)
        return size

    def readlen(self, length):
        buf = self.file.read(length)
        if len(buf) == length:
            return buf
        else:
            raise UnexpectedEOF(
                'End of file reached after {0} bytes.'.format(len(buf)))

    def scan_file(self):
        header = self.readlen(4)
        if header == b'RIFF':
            length, list_type = struct.unpack('<I4s', self.readlen(8))
            chunks = self.scan_chunks(length-4)
            self.chunks.append(RiffIndexList(header, list_type, file=self.file,
                                             position=0, chunks=chunks))
        else:
            raise Exception('Not a RIFF file!')

    def scan_chunks(self, data_length):
        chunks = []
        total_length = 0
        while total_length < data_length:
            header = self.readlen(4)
            total_length += 4

            length, = struct.unpack('<I', self.file.read(4))
            total_length += length + 4  # add 4 for itself

            position = self.file.tell()

            if header in list_headers:
                list_type = self.readlen(4)
                data = self.scan_chunks(length-4)
                if length % 2:
                    # Padding byte
                    self.file.seek(1, os.SEEK_CUR)
                    total_length += 1
                chunks.append(RiffIndexList(header, list_type, file=self.file,
                                            position=position, chunks=data))
            else:
                self.file.seek(length, os.SEEK_CUR)
                if length % 2:
                    # Padding byte
                    self.file.seek(1, os.SEEK_CUR)
                    total_length += 1
                chunks.append(RiffIndexChunk(
                    self.file, header, length, position))
        return chunks

    def close(self):
        self.file.close()
