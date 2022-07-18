#Author: Akash Bora
def Datamosh(filename,outfile,s,e,p,fps):
    def write_frame(frame):
        out_file.write(frame_start + frame)
    def mosh_delta_repeat(n_repeat):
        if n_repeat=="1":
            n_repeat=2
        repeat_frames = []
        repeat_index = 0
        for index, frame in enumerate(frames):
            if (frame[5:8] != iframe and frame[5:8] != pframe) or not start_frame <= index < end_frame:
                write_frame(frame)
                continue
            if len(repeat_frames) < n_repeat and frame[5:8] != iframe:
                repeat_frames.append(frame)
                write_frame(frame)
            elif len(repeat_frames) == n_repeat:
                write_frame(repeat_frames[repeat_index])
                repeat_index = (repeat_index + 1) % n_repeat
            else:
                write_frame(frame)
    start_frame = s
    end_frame = e
    if end_frame==1:
        end_frame=1000
    input_avi = filename
    delta = p
    in_file = open(input_avi, 'rb')
    output_avi= outfile
    in_file_bytes = in_file.read()
    out_file = open(output_avi, 'wb')
    frame_start = bytes.fromhex('30306463')
    frames = in_file_bytes.split(frame_start)
    out_file.write(frames[0])
    frames = frames[1:]
    iframe = bytes.fromhex('0001B0')
    pframe = bytes.fromhex('0001B6')
    n_video_frames = len([frame for frame in frames if frame[5:8] == iframe or frame[5:8] == pframe])
    if end_frame < 0:
        end_frame = n_video_frames
    mosh_delta_repeat(delta)
    in_file.close()
    out_file.close()
