#Author: Akash Bora
import subprocess
def Datamosh(filename, outf, s, e, p, fps=30):   
    END_FRAME_HEX = b'00dc'
    I_FRAME_HEX = b'\x00\x01\xb0'
    def main(filename, effect_sec_list, p_frames_mult):
        mosh(effect_sec_list, p_frames_mult)
    def mosh(effect_sec_list, p_frames_mult):
        with open(filename, 'rb') as in_file, open(outf, 'wb') as out_file:
            frames = split_file(in_file, END_FRAME_HEX)
            for index, frame in enumerate(frames):
                if not is_need_effect_here(index / fps, effect_sec_list):
                    out_file.write(frame + END_FRAME_HEX)
                    continue
                if not is_iframe(frame):
                    out_file.write((frame + END_FRAME_HEX) * p_frames_mult)
    def split_file(fp, marker, blocksize=4096):
        buffer = b''
        for block in iter(lambda: fp.read(blocksize), b''):
            buffer += block
            while True:
                markerpos = buffer.find(marker)
                if markerpos == -1:
                    break
                yield buffer[:markerpos]
                buffer = buffer[markerpos + len(marker):]
        yield buffer
    def is_need_effect_here(curr_sec, effect_sec_list):
        return any(start < curr_sec < end for start, end in effect_sec_list)
    def is_iframe(frame):
        return frame[5:8] == I_FRAME_HEX
    start=s
    end=e
    pf=p
    main(filename,[(start,end)],pf)
