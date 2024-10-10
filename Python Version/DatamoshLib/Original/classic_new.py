#Author: Akash Bora
def Datamosh(filename,outfile,s,e,fps):
    def mosh_iframe_removal():
        for index, frame in enumerate(frames):
            if index < start_frame or end_frame < index or frame[5:8] != iframe:
                out_file.write(frame_start + frame)
        
    start_frame = s
    end_frame = e
    if end_frame==1:
        end_frame=1000
    input_avi = filename
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
    mosh_iframe_removal()
    in_file.close()
    out_file.close()
