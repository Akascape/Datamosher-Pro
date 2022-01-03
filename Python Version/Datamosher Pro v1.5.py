import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import tkinter
import sys
import random
import re
import struct
import time
import webbrowser
from itertools import chain, repeat, islice
import subprocess
import pkg_resources
import json
#Note that this program is optimised for only windows, for other systems you have to change the ffmpeg path(line 54)
#Also get the correct version of ffglitch and extract it in the ffglitch folder!
required = {'imageio', 'imageio-ffmpeg', 'numpy'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
missingset=[*missing,]
if missing:
    res=messagebox.askquestion("Module Error","Some modules are not installed \n do you want to download and install them?")
    if res=="yes":
        try:
            for x in range(len(missingset)):
                y=missingset[x]
                subprocess.Popen('python -m pip install '+y)
            messagebox.showinfo("Module Installed","Please restart the program!")
            import imageio
            import numpy as np
        except:
            messagebox.showerror("Error downloading modules","Please download the neccessary modules separately!\n Required: Imageio, Imageio-ffmpeg")
            sys.exit()
    elif res=="no":
        messagebox.showerror("Error","Required modules not available!\nWithout the modules you can't use this program. Please install them first!")
        sys.exit()
else:
    import imageio
    import numpy as np
if os.path.isdir("pymosh") and os.path.isdir("ffglitch") and os.path.isdir("Assets"):
    from pymosh import Index
    from pymosh.codec.mpeg4 import is_iframe
else:
    messagebox.showerror("Missing Folder!","Some folder(s) are not available! Please download it from our github page.")
    sys.exit()
def resource_path0(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
#ffmpeg path:
python_folder=os.path.dirname(sys.executable)
path=python_folder.replace(os.sep, '/')
global resource, ffgac, ffedit
resource=resource_path0(path+"/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win64-v4.2.2")
ffgac=resource_path0("ffglitch/ffgac")
ffedit=resource_path0("ffglitch/ffedit")
def openfile():
    global file
    file=tkinter.filedialog.askopenfilename(filetypes =[('Video', ['*.mp4','*.avi','*.mov','*.mkv','*wmv','*gif']),('All Files', '*.*')])
    if(len(file)>1):
        LocationError.config(text=file, fg="green")
        if (len(file)>80):
            LocationError.config(text=file[:-40]+"...", fg="green")
        OpeningFile['text']='Open Again'
        OpeningFile['bg']='#D0CECE'
    else:
        LocationError.config(text="Choose Video To Datamosh", fg="red")
        OpeningFile['text']="OPEN"
        OpeningFile['bg']='#82CC6C'
def datafile():
    global vecfile
    vecfile=tkinter.filedialog.askopenfilename(filetypes =[('Video', ['*.mp4','*.avi','*.mov','*.mkv','*wmv','*gif']),('All Files', '*.*')])
    if(len(vecfile)>1):
        Opening_vector['text']='Open Again'
        Opening_vector['bg']='#D0CECE'
    else:
        Opening_vector['text']="OPEN"
        Opening_vector['bg']='#82CC6C'
def convertffmpeg(inputpath):
    Wait.config(text="Converting the Video...", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
    root.update()
    fps=30
    targetformat='.avi'
    outputpath=os.path.splitext(inputpath)[0]+'_datamoshed'+targetformat
    if var5.get()==1:
        subprocess.call(f'"{resource}" -loglevel error -y -i "{inputpath}" -crf 0 -bf 0 -b 10000k -r {fps} "{outputpath}"', shell=True)
    else:
        subprocess.call(f'"{resource}" -loglevel error -y -i "{inputpath}" -crf 0 -bf 0 -r {fps} "{outputpath}"', shell=True)
    try:
        choice=modechoices.get()
        if (choice==modes[16]):
            Wait.config(text="Applying Effect: Repeat", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            repeat(outputpath,inputpath)
        else:
            Wait.config(text="Applying Effect: Classic", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            Datamoshclassic(outputpath,inputpath)
    except:
        messagebox.showerror("FAILED","The video file or the input data have \n some issues!")
        os.remove(outputpath)
        end()
def convert(inputpath,targetformat):
    global outputpath, highest
    try:
        Wait.config(text="Converting the Video...", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update()
        outputpath=os.path.splitext(inputpath)[0]+'_datamoshed'+targetformat
        x=os.path.splitext(file)[1]
        choice = modechoices.get()
        if ((x==".gif") or (choice==modes[17]) or (choice==modes[18])or (choice==modes[19])
        or (choice==modes[20]) or (choice==modes[21]) or (choice==modes[22]) or (choice==modes[23])
        or (choice==modes[24]) or (choice==modes[25]) or (choice==modes[26]) or (choice==modes[27])
        or (choice==modes[28]) or (choice==modes[29])):
            highest="no"
        else:
            pass
        if highest=="yes":
            reader=imageio.get_reader(inputpath)
            fps=reader.get_meta_data()['fps']
            writer= imageio.get_writer(outputpath, fps=fps)
            for frames in reader:
                writer.append_data(frames)
            writer.close()
            if var5.get()==1:
                highest="yes"
            else:
                highest="no"
        elif highest=="no":
            if ((choice==modes[17]) or (choice==modes[18]) or (choice==modes[19]) or
            (choice==modes[20]) or (choice==modes[21]) or (choice==modes[22]) or
            (choice==modes[23]) or (choice==modes[24]) or (choice==modes[25]) or (choice==modes[26]) or (choice==modes[27]) or (choice==modes[28]) or (choice==modes[29])):
                subprocess.call(f'"{resource}" -hwaccel auto -i "{inputpath}" -c:v libx264 -preset medium -b:v 2M -minrate 2M -maxrate 2M -bufsize 2M -y "{outputpath}"', shell=True)
            else:
                subprocess.call(f'"{resource}" -loglevel error -y -i "{inputpath}" "{outputpath}"', shell=True)
        try:
            Datamosh(outputpath)
        except:
            pass   
    except:
        messagebox.showerror("FAILED","The video file or the input data have \n some issues!")
        os.remove(outputpath)
        end()
def validate():
    try:
        float(Countframe.get())
        float(Positframe.get())
        float(firstframes.get())
        float(killframe.get())
        x=float(killframe.get())
        if x>1:
            var4.set(1)
    except ValueError:
        messagebox.showerror("Invalid Input","Please enter some valid data")
        sys.exit()
def checkexist(file):
    mode = modechoices.get()
    tformat=exportbox.get()
    f=os.path.splitext(file)[0]
    exfile=f+"_datamoshed"+"-"+mode+"_datamoshed."+tformat
    if os.path.exists(exfile):
        warn=messagebox.askquestion("Warning","Do you want to replace the old file?")
        if warn=='yes':
            os.remove(exfile)
        elif warn=='no':
            os.kill(checkesist())
    pass
def end():
    datamoshbtn['state']=NORMAL
    modechoices['state']=NORMAL
    exportbox['state']=NORMAL
    OpeningFile['state']=NORMAL
    Highbox['state']=NORMAL
    advancedbox['state']=NORMAL
    Opening_vector['state']=NORMAL
    root.config(cursor="")
    Wait.config(text=" ", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
    root.update()  
def Step1():
    try:
        if (OpeningFile['text']=='Open Again'):
            Wait.place(relx=0.5,rely=0.85,anchor='center')
            root.update()
            datamoshbtn['state']=DISABLED
            modechoices['state']=DISABLED
            exportbox['state']=DISABLED
            OpeningFile['state']=DISABLED
            Highbox['state']=DISABLED
            advancedbox['state']=DISABLED
            Opening_vector['state']=DISABLED
            extension=os.path.splitext(file)[1]
            validate()
            checkexist(file)
            root.config(cursor="")
            choice = modechoices.get()
            if(choice==modes[7]) or (choice==modes[16]):         
                    if extension==".mp4":
                        convertffmpeg(file)
                    else:
                        targetformat=".mp4"
                        convert(file,targetformat)
                        convertffmpeg(file)
            elif(choice==modes[8]) or (choice==modes[9]) or (choice==modes[11]):
                    pymosh_library(file)
            elif((choice==modes[13]) or (choice==modes[14]) or (choice==modes[15]) or (choice==modes[17])
            or (choice==modes[18]) or (choice==modes[19]) or (choice==modes[20]) or (choice==modes[21])
            or (choice==modes[22]) or (choice==modes[23]) or (choice==modes[24]) or (choice==modes[25])
            or (choice==modes[26]) or (choice==modes[27]) or (choice==modes[28]) or (choice==modes[29])):
                    if (choice==modes[15]):
                        if (Opening_vector['text']=='Open Again'):
                            wrong.place_forget()
                            pass
                        elif (Opening_vector['text']=="OPEN"):
                            wrong.place(x=250,y=235)
                            os.kill(Step1)
                    ffglitch_library(file)
            else:
                targetformat=".avi"
                convert(file,targetformat)
        else:
            os.kill(Step1)
    except:
        messagebox.showerror("","Please choose the video file again!")
        end()
def get_vectors(input_video):
    subprocess.call(f'"{ffgac}" -i "{input_video}" -an -mpv_flags +nopimb+forcemv -qscale:v 0 -g 1000' +
                    ' -vcodec mpeg2video -f rawvideo -y tmp.mpg', shell=True)
    subprocess.call(f'"{ffedit}" -i tmp.mpg -f mv:0 -e tmp.json', shell=True)
    os.remove('tmp.mpg')
    f = open('tmp.json', 'r')
    raw_data = json.load(f)
    f.close()
    os.remove('tmp.json')
    frames = raw_data['streams'][0]['frames']
    vectors = []
    for frame in frames:
        try:
            vectors.append(frame['mv']['forward'])
        except:
            vectors.append([])
    return vectors
def apply_vectors(vectors, input_video, output_video, method='add'):
    subprocess.call(f'"{ffgac}" -i "{input_video}" -an -mpv_flags +nopimb+forcemv -qscale:v 0 -g 1000' +
                    ' -vcodec mpeg2video -f rawvideo -y tmp.mpg', shell=True)
    to_add = '+' if method == 'add' else ''
    script_path = 'apply_vectors.js'
    script_contents = '''
    var vectors = [];
    var n_frames = 0;
    function glitch_frame(frame) {
        let fwd_mvs = frame["mv"]["forward"];
        if (!fwd_mvs || !vectors[n_frames]) {
            n_frames++;
            return;
        }
        for ( let i = 0; i < fwd_mvs.length; i++ ) {
            let row = fwd_mvs[i];
            for ( let j = 0; j < row.length; j++ ) {
                let mv = row[j];
                try {
                    mv[0] ''' + to_add + '''= vectors[n_frames][i][j][0];
                    mv[1] ''' + to_add + '''= vectors[n_frames][i][j][1];
                } catch {}
            }
        }
        n_frames++;
    }
    '''
    with open(script_path, 'w') as f:
        f.write(script_contents.replace('var vectors = [];', f'var vectors = {json.dumps(vectors)};'))
    subprocess.call(f'"{ffedit}" -i tmp.mpg -f mv -s "{script_path}" -o "{output_video}"', shell=True)
    os.remove('apply_vectors.js')
    os.remove('tmp.mpg')
def average(frames):
    if not frames:
        return []
    return np.mean(np.array([x for x in frames if x != []]), axis=0).tolist()
def fluid(frames):
    average_length = int(Positframe.get())
    if average_length==1:
        average_length=2
    return [average(frames[i + 1 - average_length: i + 1]) for i in range(len(frames))]
def movement(frames):
    for frame in frames:
        if not frame:
            continue
        for row in frame:
            for col in row:
                col[0] = 0
    return frames
def external_scripts(output_video):
    gop_period = int(Countframe.get())
    if (gop_period==1):
        gop_period=1000
    script_path = "ffglitch/jscripts/"+modechoices.get()+".js"
    input_video = file
    subprocess.call(f'"{ffgac}" -i "{input_video}" -an -mpv_flags +nopimb+forcemv -qscale:v 0  -b:v 20M -minrate 20M -maxrate 20M -bufsize 2M -g "{gop_period}"' +
                        ' -vcodec mpeg2video -f rawvideo -y tmp.mpg', shell=True)
    subprocess.call(f'"{ffedit}" -i tmp.mpg -f mv -s "{script_path}" -o "{output_video}"', shell=True)
    os.remove('tmp.mpg')
def ffglitch_library(file):
    choice = modechoices.get()
    outpath=os.path.dirname(file)
    outx=os.path.basename(file).split('.')[0]
    if(choice==modes[15]):
        Wait.config(text="Applying Effect: Motion Transfer", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update()
        output=outpath+"/"+outx+"_datamoshed-motion.mp4"
        extract_from=vecfile
        transfer_to=file
        vectors = []
        if extract_from:
            vectors = get_vectors(extract_from)
            if transfer_to == '':
                with open(output, 'w') as f:
                    json.dump(vectors, f)
        apply_vectors(vectors, transfer_to, output)
    elif(choice==modes[14]):
        Wait.config(text="Applying Effect: Stretch", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update()
        input_video = file
        output= outpath+"/"+outx+"_datamoshed-stretch.mp4"
        apply_vectors(movement(get_vectors(input_video)), input_video, output, method='')
    elif(choice==modes[13]):
        Wait.config(text="Applying Effect: Fluid", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update()
        input_video = file
        output= outpath+"/"+outx+"_datamoshed-fluid.mp4"
        apply_vectors(fluid(get_vectors(input_video)), input_video, output, method='')
    elif((choice==modes[13]) or (choice==modes[14]) or (choice==modes[15]) or (choice==modes[17])
        or (choice==modes[18]) or (choice==modes[19]) or (choice==modes[20]) or (choice==modes[21])
        or (choice==modes[22]) or (choice==modes[23]) or (choice==modes[24]) or (choice==modes[25])
        or (choice==modes[26]) or (choice==modes[27]) or (choice==modes[28]) or (choice==modes[29])):
        Wait.config(text="Applying Effect: "+modechoices.get(), fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update()
        output= outpath+"/"+outx+"_datamoshed-"+(modechoices.get()).lower()+".mpg"
        external_scripts(output)
    export(output)
def pymosh_library(file):
    global final
    outpath=os.path.dirname(file)
    outx=os.path.basename(file).split('.')[0]
    infile=os.path.dirname(file)+"/"+outx+"_datamoshed.avi"
    if os.path.exists(infile):
        os.remove(infile)
    fps=30
    Wait.config(text="Converting the Video...", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
    root.update()
    subprocess.call(f'"{resource}" -loglevel error -y -i "{file}" -crf 0 -bf 0 -r {fps} "{infile}"', shell=True)
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
    def avi_sort(filename, outfile):
        f = Index.from_file(filename)
        for stream in f.video:
            sorted_stream = sorted(stream, key=len, reverse=True)
            stream.replace(sorted_stream)
        f.rebuild()
        with open(outfile, 'wb') as out:
            f.write(out)
    def process_streams(in_filename, out_filename, func, *args, **kwargs):
            f = Index.from_file(in_filename)
            for stream in f.video:
                midpoint=float(firstframes.get())
                if midpoint>1:
                    midpoint=1
                drifted = list(func(stream, midpoint,*args, **kwargs))
                stream.replace(drifted)
            f.rebuild()
            with open(out_filename, 'wb') as out:
                f.write(out)
    def echo(stream, midpoint):
        all_frames = list(stream)
        pframes = [f for f in all_frames if not is_iframe(f)]
        midpoint_idx = int(len(all_frames)*midpoint)
        frames = all_frames[:midpoint_idx]
        while len(frames) < len(all_frames):
            frames += pframes[:(len(all_frames) - len(frames))]
        return frames
    choice = modechoices.get()
    if(choice==modes[8]):
        Wait.config(text="Applying Effect: Glide", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update()
        time.sleep(2)
        interval=int(Positframe.get())
        if (interval==1):
            interval=2
        outfile=outpath+"/"+os.path.basename(infile).split('.')[0]+"-glide.avi"
        if os.path.exists(outfile):
            os.remove(outfile)
        glide(interval, infile, outfile)
    elif (choice==modes[9]):
        Wait.config(text="Applying Effect: Sort", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update()
        time.sleep(2)
        outfile=outpath+"/"+os.path.basename(infile).split('.')[0]+"-sort.avi"
        if os.path.exists(outfile):
            os.remove(outfile)
        avi_sort(infile, outfile)
    elif (choice==modes[11]):
        Wait.config(text="Applying Effect: Echo", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update()
        time.sleep(2)
        outfile=outpath+"/"+os.path.basename(infile).split('.')[0]+"-echo.avi"
        if os.path.exists(outfile):
            os.remove(outfile)
        process_streams(infile, outfile, echo)
    final=outpath+"/"+os.path.basename(outfile).split('.')[0]+".mp4"
    if os.path.exists(final):
            os.remove(final)
    subprocess.call(f'"{resource}" -loglevel error -y -i "{outfile}" "{final}"', shell=True)
    export2=exportbox.get()
    os.remove(infile)
    export(final)
    os.remove(outfile)
def repeat(filename, mainfile):
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
    fps=30
    start_frame = int(firstframes.get())
    end_frame = int(Countframe.get())
    if end_frame==1:
        end_frame=1000
    input_avi = filename
    delta = int(Positframe.get())
    in_file = open(input_avi, 'rb')
    outx=os.path.basename(filename).split('.')[0]
    outpath=os.path.dirname(mainfile) 
    output_avi=outpath+"/"+outx+"-repeat.avi"
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
    out=outpath+"/"+outx+"-repeat.mp4"
    subprocess.call(f'"{resource}" -loglevel error -y -i "{output_avi}" "{out}"', shell=True)
    export2=exportbox.get()
    in_file.close()
    out_file.close()
    if(export2==exportchoices[0]):
        pass
    else:
        os.remove(output_avi)
    os.remove(filename)
    export(out)
def Datamoshclassic(filename,mainfile):   
    global outf
    END_FRAME_HEX = b'00dc'
    I_FRAME_HEX = b'\x00\x01\xb0'
    fps=30
    outx=os.path.basename(filename).split('.')[0]
    outpath=os.path.dirname(mainfile) 
    outf=outpath+"/"+outx+"-classic_datamoshed.avi"
    def main2(filename, effect_sec_list, p_frames_mult):
        magic(effect_sec_list, p_frames_mult)
        out=outpath+"/"+outx+"-classic.mp4"
        subprocess.call(f'"{resource}" -loglevel error -y -i "{outf}" "{out}"', shell=True)
        os.remove(filename)
        export(out)
        export2=exportbox.get()
        if(export2==exportchoices[0]):
            pass
        else:
            os.remove(outf)
    def magic(effect_sec_list, p_frames_mult):
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
    start=float(firstframes.get())
    make=float(Countframe.get())
    timer=int(Positframe.get())
    main2(filename,[(start,make)],timer)
def Datamosh(Inputfile):
  global fileout
  checkinput=os.path.splitext(file)[0]+"_datamoshed.avi"
  if os.path.exists(checkinput):
    filein = Inputfile
    countframes = int(Countframe.get())
    positframes = int(Positframe.get())
    firstframe = int(firstframes.get())
    choice = modechoices.get()
    kill = float(killframe.get())
    audio=0
    if(choice==modes[0]):
            mode="bloom"
    elif(choice==modes[1]):
            mode="invert"
    elif(choice==modes[2]):
            mode="jiggle"
    elif(choice==modes[3]):
            mode="overlap"
    elif(choice==modes[4]):
            mode="pulse"
    elif(choice==modes[5]):
            mode="reverse"
    elif(choice==modes[6]):
            mode="random"
    elif(choice==modes[10]):
            mode="shake"
    elif(choice==modes[12]):
            mode="void"
    else:
        messagebox.showerror("Error!","Please select a valid mode!")
        os.remove(outputpath)
        end()
        os.kill(Datamosh())
    temp_nb = random.randint(10000, 99999)
    temp_dir = "temp-" + str(temp_nb)
    temp_hdrl = temp_dir +"/hdrl.bin"
    temp_movi = temp_dir +"/movi.bin"
    temp_idx1 = temp_dir +"/idx1.bin"    
    os.mkdir(temp_dir)
    def constrain(val, min_val, max_val):
        return min(max_val, max(min_val, val))
    def bstream_until_marker(bfilein, bfileout, marker=0, startpos=0):
            chunk = 1024
            filesize = os.path.getsize(bfilein)
            if marker :
                    marker = str.encode(marker)

            with open(bfilein,'rb') as rd:
                    with open(bfileout,'ab') as wr:
                            for pos in range(startpos, filesize, chunk):
                                    rd.seek(pos)
                                    buffer = rd.read(chunk)

                                    if marker:
                                            if buffer.find(marker) > 0 :
                                                    marker_pos = re.search(marker, buffer).start()
                                                    marker_pos = marker_pos + pos
                                                    split = buffer.split(marker, 1)
                                                    wr.write(split[0])
                                                    return marker_pos
                                            else:
                                                    wr.write(buffer)
                                    else:
                                            wr.write(buffer)
    movi_marker_pos = bstream_until_marker(filein, temp_hdrl, "movi")
    idx1_marker_pos = bstream_until_marker(filein, temp_movi, "idx1", movi_marker_pos)
    bstream_until_marker(filein, temp_idx1, 0, idx1_marker_pos)
    with open(temp_movi,'rb') as rd:
            chunk = 1024
            filesize = os.path.getsize(temp_movi)
            frame_table = []
            for pos in range(0, filesize, chunk):
                    rd.seek(pos)
                    buffer = rd.read(chunk)
                    for m in (re.finditer(b'\x30\x31\x77\x62', buffer)):
                                    if audio : frame_table.append([m.start() + pos, 'sound'])		
                    for m in (re.finditer(b'\x30\x30\x64\x63', buffer)):
                            frame_table.append([m.start() + pos, 'video'])
                    frame_table.sort(key=lambda tup: tup[0])
            l = []
            l.append([0,0, 'void'])
            max_frame_size = 0
            for n in range(len(frame_table)):
                    if n + 1 < len(frame_table):
                            frame_size = frame_table[n + 1][0] - frame_table[n][0]
                    else:
                            frame_size = filesize - frame_table[n][0]
                    max_frame_size = max(max_frame_size, frame_size)
                    l.append([frame_table[n][0],frame_size, frame_table[n][1]])
    clean = []
    final = []
    if firstframe :
            for x in l :
                    if x[2] == 'video':
                            clean.append(x)
                            break
    for x in l:
            if x[1] <= (max_frame_size * kill) :
                    clean.append(x)
    if mode == "void":
            Wait.config(text="Applying Effect: Void", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            final = clean
    if mode == "random":
            Wait.config(text="Applying Effect: Random", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            final = random.sample(clean,len(clean))
    if mode == "reverse":
            Wait.config(text="Applying Effect: Reverse", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            final = sum(zip(clean[::-1], clean[:-1]), ())
    if mode == "invert":
            Wait.config(text="Applying Effect: Invert", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            final = sum(zip(clean[1::2], clean[::2]), ())
    if mode == 'bloom':
            Wait.config(text="Applying Effect: Bloom", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            repeat = int(countframes)
            frame = int(positframes)
            lista = clean[:frame]
            listb = clean[frame:]
            final = lista + ([clean[frame]]*repeat) + listb
    if mode == 'pulse':
            Wait.config(text="Applying Effect: Pulse", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            pulselen = int(countframes)
            pulseryt = int(positframes)
            j = 0
            for x in clean:
                    i = 0
                    if(j % pulselen == 0):
                            while i < pulselen :
                                    final.append(x)
                                    i = i + 1
                    else:
                            final.append(x)
                            j = j + 1
    if mode == "jiggle":
            Wait.config(text="Applying Effect: Jiggle", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            amount = int(positframes)
            final = [clean[constrain(x+int(random.gauss(0,amount)),0,len(clean)-1)] for x in range(0,len(clean))]
    if mode == "overlap":
            Wait.config(text="Applying Effect: Overlap", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            pulselen = int(countframes)
            pulseryt = int(positframes)
            clean = [clean[i:i+pulselen] for i in range(0,len(clean),pulseryt)]
            final = [item for sublist in clean for item in sublist]
    if mode == "shake":
            Wait.config(text="Applying Effect: Shake", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            def process_streams(in_filename, out_filename, func, *args, **kwargs):
                f = Index.from_file(in_filename)
                for stream in f.video:
                    drifted = list(func(stream, *args, **kwargs))
                    stream.replace(drifted)
                f.rebuild()
                with open(out_filename, 'wb') as out:
                    f.write(out)
            def shake(stream):
                def glitch(stream):
                    all_frames = iter(stream)
                    yield next(all_frames)
                    while True:
                        frame = next(all_frames)
                        if not is_iframe(frame):
                            yield frame
                            yield frame
                return islice(glitch(stream), len(stream))
            fileout= filein[:-4] + '-' + mode + '.avi'
            process_streams(filein, fileout, shake)
            fps=30
            output= fileout[:-9]+"shake.mp4"
            subprocess.call(f'"{resource}" -loglevel error -y -i "{fileout}" -crf 0 -bf 0 -r {fps} "{output}"', shell=True)
            time.sleep(2)
            os.remove(fileout)
            os.remove(filein)
            os.remove(temp_hdrl)
            os.remove(temp_movi)
            os.remove(temp_idx1)
            os.rmdir(temp_dir)
            export(output)
            os.kill(datamosh)
    time.sleep(2)
    fileout= filein[:-4] + '-' + mode + '.avi'
    if os.path.exists(fileout):
            os.remove(fileout)
    bstream_until_marker(temp_hdrl, fileout)
    with open(temp_movi,'rb') as rd:
            filesize = os.path.getsize(temp_movi)
            with open(fileout,'ab') as wr:
                    wr.write(struct.pack('<4s', b'movi'))
                    for x in final:
                            if x[0] != 0 and x[1] != 0:
                                    rd.seek(x[0])
                                    wr.write(rd.read(x[1]))
    bstream_until_marker(temp_idx1, fileout)
    if os.path.exists(outputpath):
            os.remove(outputpath)
    else:
        pass
    os.remove(temp_hdrl)
    os.remove(temp_movi)
    os.remove(temp_idx1)
    os.rmdir(temp_dir)
    export(fileout)
  else:
      Wait.config(text="Moshed Video is Ready!", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
      root.update()
def export(fileout):
    def removefileout():
        if os.path.exists(fileout):
                    os.remove(fileout)
                    messagebox.showinfo("DONE","Datamoshed video is ready!")
                    end()
        else:
            pass
    export=exportbox.get()
    if(export==exportchoices[0]):
      ask=messagebox.askquestion("?","Do you want the Raw moshed version?")
      if ask=='yes':
        choice = modechoices.get()
        if(choice==modes[7]) or (choice==modes[16]):
            os.remove(fileout)
            Wait.config(text="Moshed Video is Ready!", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            messagebox.showinfo("DONE","Datamoshed video is ready!")
            end()
        else:
            file2=os.path.splitext(fileout)[0]
            os.rename(fileout,file2+"_datamoshed.avi")
            Wait.config(text="Moshed Video is Ready!", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            messagebox.showinfo("DONE","Datamoshed video is ready!")
            end()
      elif ask=='no':
            targetformat=".avi"
            convert(fileout,targetformat)
            removefileout()
    elif(export==exportchoices[1]):
        choice = modechoices.get()
        if(choice==modes[7]) or (choice==modes[8]) or (choice==modes[9]) or (choice==modes[16]):
            nfile=os.path.splitext(fileout)[0]
            os.rename(fileout,nfile+"_datamoshed.mp4")
            Wait.config(text="Moshed Video is Ready!", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            messagebox.showinfo("DONE","Datamoshed video is ready!")
            end()
        else: 
            targetformat=".mp4"
            convert(fileout,targetformat)
            removefileout()
    elif(export==exportchoices[2]):
            targetformat=".gif"
            convert(fileout,targetformat)
            removefileout()
    elif(export==exportchoices[3]):
            targetformat=".mov"
            convert(fileout,targetformat)
            removefileout()
    elif(export==exportchoices[4]):
            targetformat=".mkv"
            convert(fileout,targetformat)
            removefileout()
    elif(export==exportchoices[5]):
            targetformat=".wmv"
            convert(fileout,targetformat)
            removefileout()
    else:
        messagebox.showerror("Error!","Please select a valid video format!")
        os.remove(fileout)
        end()
        os.kill(Datamosh())
def toggle():
    if var.get()==0:
        Disableadvanced()
    else:
        Enableadvanced()
def Enableadvanced():
        choice = modechoices.get()
        if(choice==modes[8]) or (choice==modes[13]):
            var2.set(6)
            var4.set(0.7)
            var1.set(1)
            if (choice==modes[13]):
                var2.set(10)
            countlabel['fg']="grey"
            positlabel['fg']="green"
            firstflabel['fg']="grey"
            killlabel['fg']="grey"
            Countframe['state']=DISABLED
            Positframe['state']=NORMAL
            firstframes['state']=DISABLED
            killframe['state']=DISABLED
        elif(choice==modes[7]) or (choice==modes[16]):
            var2.set(1)
            var1.set(1000)
            if (choice==modes[16]):
                var2.set(5)
            countlabel['fg']="green"
            positlabel['fg']="green"
            firstflabel['fg']="green"
            killlabel['fg']="grey"
            Countframe['state']=NORMAL
            Positframe['state']=NORMAL
            firstframes['state']=NORMAL
            killframe['state']=DISABLED
        elif(choice==modes[6]) or (choice==modes[10]) or (choice==modes[12]):
            var2.set(1)
            var1.set(1)
            if (choice==modes[12]):
                var4.set(0.2)
            else:
                var4.set(0.7)
            var3.set(1)
            countlabel['fg']="grey"
            positlabel['fg']="grey"
            firstflabel['fg']="green"
            killlabel['fg']="green"
            Countframe['state']=DISABLED
            Positframe['state']=DISABLED
            firstframes['state']=NORMAL
            killframe['state']=NORMAL
        elif(choice==modes[5]) or (choice==modes[1]):
            var2.set(1)
            var3.set(1)
            var1.set(1)
            var4.set(0.7)
            countlabel['fg']="grey"
            positlabel['fg']="grey"
            firstflabel['fg']="green"
            killlabel['fg']="grey"
            Countframe['state']=DISABLED
            Positframe['state']=DISABLED
            firstframes['state']=NORMAL
            killframe['state']=NORMAL
        elif(choice==modes[11]):
            var2.set(1)
            var1.set(1)
            if (choice==modes[11]):
                var3.set(0.5)
            else:
                var3.set(1)
            countlabel['fg']="grey"
            positlabel['fg']="grey"
            firstflabel['fg']="green"
            killlabel['fg']="grey"
            Countframe['state']=DISABLED
            Positframe['state']=DISABLED
            firstframes['state']=NORMAL
            killframe['state']=DISABLED
        elif(choice==modes[2]):
            var2.set(1)
            var4.set(0.7)
            var1.set(1)
            countlabel['fg']="grey"
            positlabel['fg']="green"
            firstflabel['fg']="green"
            killlabel['fg']="green"
            Countframe['state']=DISABLED
            Positframe['state']=NORMAL
            firstframes['state']=NORMAL
            killframe['state']=NORMAL
        elif(choice==modes[0]) or (choice==modes[3]) or (choice==modes[4]):
            var2.set(1)
            var4.set(0.7)
            var1.set(1)
            countlabel['fg']="green"
            positlabel['fg']="green"
            firstflabel['fg']="green"
            killlabel['fg']="green"
            Countframe['state']=NORMAL
            Positframe['state']=NORMAL
            firstframes['state']=NORMAL
            killframe['state']=NORMAL
        elif((choice==modes[17]) or (choice==modes[18])
            or (choice==modes[19]) or (choice==modes[20])
            or (choice==modes[21]) or (choice==modes[22])
            or (choice==modes[23]) or (choice==modes[24])
            or (choice==modes[25]) or (choice==modes[26])
            or (choice==modes[27]) or (choice==modes[28]) or (choice==modes[29])):
            var1.set(1000)
            countlabel['fg']="green"
            positlabel['fg']="grey"
            firstflabel['fg']="grey"
            killlabel['fg']="grey"
            Countframe['state']=NORMAL
            Positframe['state']=DISABLED
            firstframes['state']=DISABLED
            killframe['state']=DISABLED
        else:
            Disableadvanced()         
def Disableadvanced():
        var1.set("1")
        var2.set(1)
        var3.set(1)
        var4.set(0.7)
        countlabel['fg']="grey"
        positlabel['fg']="grey"
        firstflabel['fg']="grey"
        killlabel['fg']="grey"
        Countframe['state']=DISABLED
        Positframe['state']=DISABLED
        firstframes['state']=DISABLED
        killframe['state']=DISABLED
def refresh(event):
    if var=="0":
        pass
    else:
        modechoices['values']=toggle()
    choice = modechoices.get()
    if (choice==modes[15]):
        vector_label.place(x=270,y=233)
        Opening_vector.place(x=350,y=233)
    else:
        vector_label.place_forget()
        Opening_vector.place_forget()
def toggle2():
    global highest
    if var5.get()==1:
        highest="yes"
    else:
        highest="yes"
def info():
    messagebox.showinfo("Help",
    "Datamosher Pro is a free tool that can mosh and corrupt video files and exports awesome glitched videos."
    "\nHow To Use:\n➤First open the video you want to datamosh."
    "\n➤Choose the desired datamosh mode, then select the export format."
    "\n➤Use advanced options for different modes (For more details about the advanced options, visit our Github page)."
    "\n➤Click on the datamosh button, then wait for a few seconds."
    "\n➤After conversion, your video will be ready and you can view the moshed video with any media player."
    "\n\nDeveloper: Akash Bora (a.k.a. Akascape)\nIf you are facing any issue then contact me on Github."
    "\nVersion-1.5")
def callback(url):
    webbrowser.open_new_tab("https://github.com/Akascape/Datamosher-Pro-GUI-.git")
root=Tk()
root.title("Datamosher Pro")
root.resizable(width=False, height=False)
root.geometry("500x450")
root.configure(bg='#FFFFFF')
root.columnconfigure(0,weight=1)
icopath=resource_path0("Assets/icon.ico")
root.wm_iconbitmap(icopath)
path=resource_path0("Assets/label.png")
LabelIMG=PhotoImage(file=path)
headlabel=Label(root,image=LabelIMG,borderwidth=0, highlightthickness=0, padx=0,pady=0)
headlabel.grid()
LocationError=Label(root,text="Choose Video To Datamosh",fg="red",bg='#FFFFFF')
LocationError.grid()
OpeningFile= Button(root, width=61,bg="#82CC6C",fg="white", text="OPEN",highlightthickness=1,borderwidth=0.2,relief="groove",command=openfile)
OpeningFile.grid()
chooselabel=Label(root,text="Select Mode:",font="Aharoni",bg='#FFFFFF')
chooselabel.place(x=80,y=115,anchor='center')
modes=["Bloom", "Invert", "Jiggle", "Overlap", "Pulse", "Reverse",
       "Random", "Classic", "Glide", "Sort", "Shake", "Echo", "Void",
       "Fluid", "Stretch", "Motion", "Repeat", "Shear", "Delay", "Sink",
       "Mirror", "Vibrate", "Slam Zoom", "Zoom","Invert-Reverse", "Shift",
       "Noise", "Stop", "Buffer", "Slice"]
modechoices=ttk.Combobox(root,values=sorted(modes), font="Verdana 12", width=10, height=10)
modechoices.current(0)
modechoices.bind('<FocusIn>', lambda event: refresh(event))
modechoices.place(x=130,y=104)
exportchoices=["AVI","MP4","GIF","MOV","MKV","WMV"]
exportlabel=Label(root,text="Export Format:",font="Aharoni",bg='#FFFFFF')
exportlabel.place(x=270,y=105)
exportbox=ttk.Combobox(root,values=exportchoices, font="Verdana 10", width=8)
exportbox.current(1)
exportbox.place(x=380,y=106)
global var
var = IntVar()
var.set(0)
advancedbox=Checkbutton(root, text="Advanced",bg="#FFFFFF", command=toggle,variable=var,onvalue=1, offvalue=0)
advancedbox.place(x=70,y=150, anchor='center')
var1=DoubleVar()
var1.set(1)
countlabel=Label(root,text="Glitch Size",fg="grey",bg='#FFFFFF')
countlabel.place(x=50,y=165)
Countframe=Entry(root,bg="#00D2FF",width=10,borderwidth=3, textvariable=var1,state=DISABLED)
Countframe.place(x=140,y=165)
var2=DoubleVar()
var2.set(1)
positlabel=Label(root,text="Frames Frequency",fg="grey",bg='#FFFFFF')
positlabel.place(x=270,y=165)
Positframe=Entry(root,bg="#00D2FF",width=10,borderwidth=3, textvariable=var2, state=DISABLED)
Positframe.place(x=380,y=165)
var3=IntVar()
var3.set(1)
firstflabel=Label(root,text="First Frame",fg="grey",bg='#FFFFFF')
firstflabel.place(x=50,y=200)
firstframes=Entry(root,bg="#00D2FF",width=10,borderwidth=3, textvariable=var3, state=DISABLED)
firstframes.place(x=140,y=200)
var4=DoubleVar()
var4.set(0.7)
killlabel=Label(root,text="Kill Frames",fg="grey",bg='#FFFFFF')
killlabel.place(x=270,y=200)
killframe=Entry(root,bg="#00D2FF",width=10,borderwidth=3, textvariable=var4, state=DISABLED)
killframe.place(x=380,y=200)
global Wait
Wait=Label(root,text="",fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
infobtn=Button(root, width=2,bg="#FFFFFF",fg="black", text="ⓘ",font=(10),relief="sunken",cursor='hand2', highlightthickness=0,borderwidth=0,padx=0,pady=0,command=info)
infobtn.place(x=475,y=425)
dev=Label(root, text='Developed by Akascape | For more info, visit:',bg='#FFFFFF',fg="#6D76CD", font=("Impact",10))
dev.place(x=5,y=430)
link=Label(root, text="Datamosher Pro Github",font=('Impact',10),bg='#FFFFFF',fg="#6D76CD", cursor="hand2")
link.place(x=245,y=430)
link.bind("<Button-1>", lambda e:
callback("https://github.com/Akascape/Datamosher-Pro-GUI-.git"))
path0=resource_path0("Assets/button.png")
buttonIMG=PhotoImage(file=path0)
datamoshbtn=Button(root,image=buttonIMG,borderwidth=0, highlightthickness=0, padx=0,pady=0,command=Step1)
datamoshbtn.place(x=100,y=270)
vector_label=Label(root,text="Vector File:",fg="green",bg='#FFFFFF')
Opening_vector= Button(root, width=15,bg="#82CC6C",fg="white", text="OPEN",highlightthickness=1,borderwidth=0.2,relief="groove",command=datafile)
global var5
var5 = IntVar()
var5.set(1)
highest="yes"
Highbox=Checkbutton(root, text="Highest Quality",bg="#FFFFFF", command=toggle2,variable=var5,onvalue=1, offvalue=0)
Highbox.place(x=85,y=240, anchor='center')
wrong=Label(root, width=2,bg="#FFFFFF",fg="red", text="ⓘ",font=(10),relief="sunken", highlightthickness=0,borderwidth=0,padx=0,pady=0)
root.mainloop()
#DEVELOPER: AKASH BORA (a.k.a Akascape)
#Version=1.5
