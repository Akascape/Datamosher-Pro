import struct

from pymosh.codec.mpeg4 import is_iframe

from . import riff


class AVIFile(object):
    """A wrapper for AVI files."""

    def __init__(self):
        self.riff = riff.RiffIndex()
        self.streams = []
        self.frame_order = []

    @staticmethod
    def from_file(filename: str):
        instance = AVIFile()

        instance.riff = riff.RiffIndex.from_file(filename=filename)

        header = instance.riff.find(b'LIST', b'hdrl')
        # Get stream info
        stream_lists = header.find_all(b'LIST', b'strl')
        for l in stream_lists:
            strh = l.find(b'strh')
            data = strh.data
            fccType, = struct.unpack(b'4s', data[:4])
            stream = Stream(len(instance.streams), fccType)
            instance.streams.append(stream)

        instance.split_streams()

        return instance

    def __iter__(self):
        return iter(self.streams)

    def add_frame(self, chunk):
        stream_num = int(chunk.header[:2])
        if stream_num < len(self.streams):
            self.frame_order.append(
                (stream_num, len(self.streams[stream_num])))
            self.streams[stream_num].add_frame(chunk)

    def split_streams(self):
        movi = self.riff.find(b'LIST', b'movi')
        for chunk in movi:
            self.add_frame(chunk)

    def combine_streams(self):
        chunks = []
        for frame_record in self.frame_order:
            stream_num, frame_num = frame_record
            stream = self.streams[stream_num]
            frame = stream[frame_num]
            chunks.append(frame)
        return chunks

    def _video(self):
        return filter(lambda stream: stream.type == b'vids', self.streams)
    video = property(_video)

    def _audio(self):
        return filter(lambda stream: stream.type == b'auds', self.streams)
    audio = property(_audio)

    def rebuild(self):
        """Rebuild RIFF tree and index from streams."""
        movi = self.riff.find(b'LIST', b'movi')
        movi.chunks = self.combine_streams()
        self.rebuild_index()

    def rebuild_index(self):
        old_index = self.riff.find(b'idx1')
        movi = self.riff.find(b'LIST', b'movi')
        data = b''
        offset = 0
        flags = {
            'base':     0x00000000,
            'keyframe': 0x00000010,
        }
        for chunk in movi:
            length = len(chunk)
            frame_flags = flags['base']
            # If it's a video keyframe or audio frame, use keyframe flag
            if (chunk.header[2] == b'd' and is_iframe(chunk)) or (chunk.header[2] == b'w'):
                frame_flags |= flags['keyframe']
            data += struct.pack(b'<4sIII', chunk.header, frame_flags, offset,
                                length+8)
            offset += length + 8 + (length % 2)
        new_index = riff.RiffDataChunk(b'idx1', data)
        self.riff.find(b'RIFF').replace(old_index, new_index)

    def write(self, fh):
        self.riff.write(fh)


class Stream(object):
    def __init__(self, num, stream_type):
        self.num = int(num)
        self.type = stream_type
        self.chunks = []

    def add_frame(self, chunk):
        self.chunks.append(chunk)

    def __getitem__(self, index):
        return self.chunks.__getitem__(index)

    def __iter__(self):
        return self.chunks.__iter__()

    def __len__(self):
        return len(self.chunks)

    def append(self, *args):
        return self.chunks.append(*args)

    def extend(self, *args):
        return self.chunks.extend(*args)

    def replace(self, chunks):
        self.chunks = chunks
