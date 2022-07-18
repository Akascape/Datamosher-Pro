#Author: Akash Bora 
from pymosh import Index
from pymosh.codec.mpeg4 import is_iframe
from itertools import islice
class library(): 
    def glide(interval, filename, outfile):
        f = Index.from_file(filename)
        buf = [None]
        def process_frame(frame):
            if buf[0] == None or not is_iframe(frame):
                buf[0] = frame
            else:
                frame = buf[0]
            return frame
        for stream in f.video:
            newstream = []
            newstream.append(stream[0])
            ix = 0
            jx = 0
            for i in stream[1:]:
                ix += 1
                jx += 1
                if ix < interval:
                    newstream.append(process_frame(stream[jx]))
                else:
                    newstream.append(newstream[-1])
                if ix > interval * 2:
                    ix = 0
        stream.replace(newstream)
        f.rebuild()
        with open(outfile, 'wb') as out:
            f.write(out)
            
    def avi_sort(filename, outfile, mode, rev):
        f = Index.from_file(filename)
        for stream in f.video:
            if mode==0:
                sorted_stream = sorted(stream, key=len, reverse=rev)
            else:
                sorted_stream = sorted(stream, key=lambda s: s[len(s)-6], reverse=rev)
            stream.replace(sorted_stream)
        f.rebuild()
        with open(outfile, 'wb') as out:
            f.write(out)
            
    def process_streams(in_filename, out_filename, mid=''):
        def echo(stream, midpoint):
            all_frames = list(stream)
            pframes = [f for f in all_frames if not is_iframe(f)]
            midpoint_idx = int(len(all_frames)*midpoint)
            frames = all_frames[:midpoint_idx]
            while len(frames) < len(all_frames):
                frames += pframes[:(len(all_frames) - len(frames))]
            return frames
        mode=echo
        f = Index.from_file(in_filename)
        for stream in f.video:
            midpoint=mid     
            drifted = list(mode(stream, midpoint))
            stream.replace(drifted)
        f.rebuild()
        with open(out_filename, 'wb') as out:
            f.write(out)

