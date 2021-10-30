import os
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import tkinter
import sys
import imageio 
import random
import re
import struct
import time
import webbrowser
from itertools import chain, repeat
import subprocess
def resource_path0(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
def openfile():
    global file
    file=tkinter.filedialog.askopenfilename(filetypes =[('MP4', '*.mp4'),('AVI', '*.avi'),('GIF','*.gif'),('MOV','*.mov')])
    if(len(file)>1):
        LocationError.config(text=file, fg="green")
        OpeningFile['text']='Open Again'
        OpeningFile['bg']='#D0CECE'
    else:
        LocationError.config(text="Choose Video To Datamosh", fg="red")
        OpeningFile['text']='OPEN'
        OpeningFile['bg']='#82CC6C'
def convertffmpeg(inputpath):
    Wait.config(text="Converting the Video...", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
    root.update()
    fps=30
    targetformat='.avi'
    #Change the imageio-ffmpeg path if not working (also in the datamoshclassic function)
    resource=resource_path0("C:/Users/User/AppData/Local/Programs/Python/Python39/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win64-v4.2.2.exe")
    outputpath=os.path.splitext(inputpath)[0]+'_datamoshed'+targetformat
    subprocess.call(f'"{resource}" -loglevel error -y -i "{inputpath}" -crf 0 -bf 0 -r {fps} "{outputpath}"', shell=True)
    try:
        Wait.config(text="Applying Effect: Classic", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update()
        Datamoshclassic(outputpath,inputpath)
    except:
        messagebox.showerror("FAILED","The video file or the input data have \n some issues!")
        Wait.place_forget()
        os.remove(outputpath)
        datamoshbtn['state']=NORMAL
        datamoshbtn['cursor']=''
def convert(inputpath,targetformat):
    global outputpath
    try:
        Wait.config(text="Converting the Video...", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
        root.update()
        outputpath=os.path.splitext(inputpath)[0]+'_datamoshed'+targetformat
        reader=imageio.get_reader(inputpath)
        fps=reader.get_meta_data()['fps']
        writer= imageio.get_writer(outputpath, fps=fps)
        for frames in reader:
            writer.append_data(frames)
            #for detailed logs of conversions, remove the comment in the next 2 lines
            #print(f'Frame {frames}')
        #print("Converted")
        writer.close()
        try:
            Datamosh(outputpath)
        except:
            pass  
    except Exception:
        messagebox.showerror("FAILED","The video file or the input data have \n some issues!")
        Wait.place_forget()
        os.remove(outputpath)
        datamoshbtn['state']=NORMAL
        datamoshbtn['cursor']=''
def Step1():
    try:
        if (len(file)>=1):
            Wait.place(relx=0.5,rely=0.85,anchor='center')
            root.update()
            extension=os.path.splitext(file)[1]
            datamoshbtn['state']=DISABLED
            datamoshbtn['cursor']='watch'
            choice = modechoices.get()           
            if(choice==modes[7]):
                    if extension==".mp4":
                        convertffmpeg(file)
                    else:
                        targetformat=".mp4"
                        convert(file,targetformat)
                        convertffmpeg(file)
            else:
                if extension==".avi":
                    Datamosh(file)
                else:    
                    targetformat=".avi"
                    convert(file,targetformat)
        else:
            messagebox.showerror("OOPS","Please choose the video again!")
    except:
        messagebox.showerror("OOPS","Please choose the video!")
        datamoshbtn['state']=NORMAL
        datamoshbtn['cursor']=''
def Datamoshclassic(filename,mainfile):
    global outf
    END_FRAME_HEX = b'00dc'
    I_FRAME_HEX = b'\x00\x01\xb0'
    fps=30
    outx=os.path.basename(filename).split('.')[0]
    outpath=os.path.dirname(mainfile)
    outf=outpath+"/"+outx+"_classic_datamoshed.avi"
    def main2(filename, effect_sec_list, p_frames_mult=1):
        magic(effect_sec_list, p_frames_mult)
        out=outpath+"/"+outx+"_classic_datamoshed.mp4"
        #Change the imageio-ffmpeg path here also if not working
        resource=resource_path0("C:/Users/User/AppData/Local/Programs/Python/Python39/Lib/site-packages/imageio_ffmpeg/binaries/ffmpeg-win64-v4.2.2.exe")
        subprocess.call(f'"{resource}" -loglevel error -y -i "{outf}" "{out}"', shell=True)
        os.remove(filename)
        export(out)
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
    start=int(firstframes.get())
    make=int(Countframe.get())
    timer=int(Positframe.get())
    main2(filename,[(start,make)],timer)
def Datamosh(Inputfile):
  if os.path.splitext(outputpath)[1]==".avi":
    filein = Inputfile
    countframes = int(Countframe.get())
    positframes = int(Positframe.get())
    firstframe = int(firstframes.get())
    choice = modechoices.get()
    kill = float(killframe.get())
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
    else:
        messagebox.showerror("OOPS","Please Select the Correct Mode!")
        os.remove(outputpath)
        os.kill(Datamosh())
        Wait.place_forget()
        datamoshbtn['state']=NORMAL
        datamoshbtn['cursor']=''
    if filein is None or os.path.exists(filein) == False:
            messagebox.showerror("ERROR","Input File is Missing!")
            Wait.place_forget()
            os.remove(outputpath)
            datamoshbtn['state']=NORMAL
            os.kill(Datamosh())
            datamoshbtn['cursor']=''
    #define temp directory and files
    temp_nb = random.randint(10000, 99999)
    temp_dir = "temp-" + str(temp_nb)
    temp_hdrl = temp_dir +"/hdrl.bin"
    temp_movi = temp_dir +"/movi.bin"
    temp_idx1 = temp_dir +"/idx1.bin"    
    os.mkdir(temp_dir)
    #Define constrain function for jiggle :3
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
                                                    marker_pos = re.search(marker, buffer).start() # position is relative to buffer glitchedframes
                                                    marker_pos = marker_pos + pos # position should be absolute now
                                                    split = buffer.split(marker, 1)
                                                    wr.write(split[0])
                                                    return marker_pos
                                            else:
                                                    wr.write(buffer)
                                    else:
                                            wr.write(buffer)
    #make 3 files, 1 for each chunk
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
        #build first list with all adresses 
                    for m in (re.finditer(b'\x30\x31\x77\x62', buffer)): # find iframes
                                    if audio : frame_table.append([m.start() + pos, 'sound'])		
                    for m in (re.finditer(b'\x30\x30\x64\x63', buffer)): # find b frames
                            frame_table.append([m.start() + pos, 'video'])
                    #then remember to sort the list
                    frame_table.sort(key=lambda tup: tup[0])
            l = []
            l.append([0,0, 'void'])
            max_frame_size = 0
    #build tuples for each frame index with frame sizes
            for n in range(len(frame_table)):
                    if n + 1 < len(frame_table):
                            frame_size = frame_table[n + 1][0] - frame_table[n][0]
                    else:
                            frame_size = filesize - frame_table[n][0]
                    max_frame_size = max(max_frame_size, frame_size)
                    l.append([frame_table[n][0],frame_size, frame_table[n][1]])
    # variables that make shit work
    clean = []
    final = []
    # keep first video frame or not
    if firstframe :
            for x in l :
                    if x[2] == 'video':
                            clean.append(x)
                            break
    # clean the list by killing "big" frames
    for x in l:
            if x[1] <= (max_frame_size * kill) :
                    clean.append(x)
    # FX modes
    if mode == "random":
            Wait.config(text="Applying Effect: Random", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            final = random.sample(clean,len(clean))
    if mode == "reverse":
            Wait.config(text="Applying Effect: Reverse", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            final = clean[::-1]
    if mode == "invert":
            Wait.config(text="Applying Effect: Invert", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            final = sum(zip(clean[1::2], clean[::2]), ())
    if mode == 'bloom':
            Wait.config(text="Applying Effect: Bloom", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            repeat = int(countframes)
            frame = int(positframes)
            ## split list
            lista = clean[:frame]
            listb = clean[frame:]
            ## rejoin list with bloom
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
    time.sleep(2)
    #name new file
    cname = '-c' + str(countframes) if int(countframes) > 1 else '' 
    pname = '-n' + str(positframes) if int(positframes) > 1 else ''
    fileout= filein[:-4] + '-' + mode + cname + pname + '.avi'
    #delete old file
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
                    Wait.place_forget()
                    datamoshbtn['state']=NORMAL
                    datamoshbtn['cursor']=''
        else:
            pass
    export=exportbox.get()
    if(export==exportchoices[0]):
        choice = modechoices.get()
        if(choice==modes[7]):
            os.remove(fileout)
            Wait.config(text="Moshed Video is Ready!", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            messagebox.showinfo("DONE","Datamoshed video is ready!")
            Wait.place_forget()
            datamoshbtn['state']=NORMAL
            datamoshbtn['cursor']=''
            os.kill(Datamoshclassic())
        else:
            Wait.config(text="Moshed Video is Ready!", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            messagebox.showinfo("DONE","Datamoshed video is ready!")
            Wait.place_forget()
            datamoshbtn['state']=NORMAL
            datamoshbtn['cursor']=''
    elif(export==exportchoices[1]):
        choice = modechoices.get()
        if(choice==modes[7]):
            Wait.config(text="Moshed Video is Ready!", fg="#6D76CD",bg='#FFFFFF', font=("Aharoni",15))
            root.update()
            messagebox.showinfo("DONE","Datamoshed video is ready!")
            Wait.place_forget()
            datamoshbtn['state']=NORMAL
            datamoshbtn['cursor']=''
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
        messagebox.showerror("OOPS","Please Select the Correct Format!")
        os.remove(outputpath)
        os.kill(Datamosh())
        Wait.place_forget()
        datamoshbtn['state']=NORMAL
        datamoshbtn['cursor']=''
def toggle():
    if var.get() == 0:
        Disableadvanced()
    else:
        Enableadvanced()
def Enableadvanced():
        choice = modechoices.get()
        if(choice==modes[7]):
            var1.set("3")
            countlabel['fg']="green"
            positlabel['fg']="green"
            firstflabel['fg']="green"
            killlabel['fg']="grey"
            Countframe['state']=NORMAL
            Positframe['state']=NORMAL
            firstframes['state']=NORMAL
            killframe['state']=DISABLED
        elif(choice==modes[6]):
            countlabel['fg']="grey"
            positlabel['fg']="grey"
            firstflabel['fg']="green"
            killlabel['fg']="green"
            Countframe['state']=DISABLED
            Positframe['state']=DISABLED
            firstframes['state']=NORMAL
            killframe['state']=NORMAL
        elif(choice==modes[5]):
            countlabel['fg']="grey"
            positlabel['fg']="grey"
            firstflabel['fg']="green"
            killlabel['fg']="grey"
            Countframe['state']=DISABLED
            Positframe['state']=DISABLED
            firstframes['state']=NORMAL
            killframe['state']=DISABLED
        elif(choice==modes[1]):
            countlabel['fg']="grey"
            positlabel['fg']="grey"
            firstflabel['fg']="green"
            killlabel['fg']="grey"
            Countframe['state']=DISABLED
            Positframe['state']=DISABLED
            firstframes['state']=NORMAL
            killframe['state']=DISABLED
        elif(choice==modes[2]):
            countlabel['fg']="grey"
            positlabel['fg']="green"
            firstflabel['fg']="green"
            killlabel['fg']="green"
            Countframe['state']=DISABLED
            Positframe['state']=NORMAL
            firstframes['state']=NORMAL
            killframe['state']=NORMAL
        else:
            var1.set("1")
            countlabel['fg']="green"
            positlabel['fg']="green"
            firstflabel['fg']="green"
            killlabel['fg']="green"
            Countframe['state']=NORMAL
            Positframe['state']=NORMAL
            firstframes['state']=NORMAL
            killframe['state']=NORMAL
def Disableadvanced():
        var1.set("1")
        countlabel['fg']="grey"
        positlabel['fg']="grey"
        firstflabel['fg']="grey"
        killlabel['fg']="grey"
        Countframe['state']=DISABLED
        Positframe['state']=DISABLED
        firstframes['state']=DISABLED
        killframe['state']=DISABLED
def info():
    messagebox.showinfo("Help",
    "Datamosher Pro is made for those who want to datamosh their video files and achieve that glitch effect."
    "\nHow To Use:\n➤First input the video you want to datamosh."
    "\n➤Choose the desired datamosh mode, then select the export format."
    "\n➤Use advance options for different modes (For more info about the advanced options, go to our Github page)."
    "\n➤Then just click on the datamosh button, then wait for a few seconds."
    "\n➤After converting, your video will be moshed and you can find the video in the directory."
    "\n➤Note that if you mosh the same files in the same location again, then the new moshed file will replace the old file."
    "\n\nDeveloper: Akash Bora (a.k.a. Akascape)\nIf you have any issue then contact me on Github.")
def callback(url):
    webbrowser.open_new_tab("https://github.com/Akascape/Datamosher-Pro-GUI-.git")
root=Tk()
root.title("Datamosher Pro")
root.resizable(width=False, height=False)
root.geometry("500x450")
root.configure(bg='#FFFFFF')
root.columnconfigure(0,weight=1)
icopath=resource_path0("icon.ico")
root.wm_iconbitmap(icopath)
path=resource_path0("label.png")
LabelIMG=PhotoImage(file=path)
headlabel=Label(root,image=LabelIMG,borderwidth=0, highlightthickness=0, padx=0,pady=0)
headlabel.grid()
LocationError=Label(root,text="Choose Video To Datamosh",fg="red",bg='#FFFFFF')
LocationError.grid()
OpeningFile= Button(root, width=60,bg="#82CC6C",fg="white", text="OPEN",highlightthickness=1,borderwidth=0.2,relief="groove",command=openfile)
OpeningFile.grid()
chooselabel=Label(root,text="Select Mode:",font="Aharoni",bg='#FFFFFF')
chooselabel.place(x=80,y=115,anchor='center')
modes=["Bloom","Invert","Jiggle", "Overlap","Pulse", "Reverse", "Random", "Classic"]
modechoices=ttk.Combobox(root,values=modes, font="Verdana 12", width=7)
modechoices.current(0)
modechoices.place(x=130,y=104)
exportchoices=["AVI(RAW)","MP4","GIF","MOV","MKV","WMV"]
exportlabel=Label(root,text="Export Format:",font="Aharoni",bg='#FFFFFF')
exportlabel.place(x=270,y=105)
exportbox=ttk.Combobox(root,values=exportchoices, font="Verdana 10", width=8)
exportbox.current(1)
exportbox.place(x=380,y=104)
var = IntVar()
var.set(0)
advancedbox=Checkbutton(root, text="Advanced",bg="#FFFFFF", command=toggle,variable=var,onvalue=1, offvalue=0)
advancedbox.place(x=70,y=150, anchor='center')
var1=IntVar()
var1.set(1)
countlabel=Label(root,text="Glitch Freqency",fg="grey",bg='#FFFFFF')
countlabel.place(x=40,y=165)
Countframe=Entry(root,bg="light blue",width=10,borderwidth=3, textvariable=var1,state=DISABLED)
Countframe.place(x=140,y=165)
var2=IntVar()
var2.set(1)
positlabel=Label(root,text="Frames Frequency",fg="grey",bg='#FFFFFF')
positlabel.place(x=270,y=165)
Positframe=Entry(root,bg="light blue",width=10,borderwidth=3, textvariable=var2, state=DISABLED)
Positframe.place(x=380,y=165)
var3=IntVar()
var3.set(1)
firstflabel=Label(root,text="Ignored Frames",fg="grey",bg='#FFFFFF')
firstflabel.place(x=40,y=200)
firstframes=Entry(root,bg="light blue",width=10,borderwidth=3, textvariable=var3, state=DISABLED)
firstframes.place(x=140,y=200)
var4=DoubleVar()
var4.set(0.7)
killlabel=Label(root,text="Kill Frames",fg="grey",bg='#FFFFFF')
killlabel.place(x=270,y=200)
killframe=Entry(root,bg="light blue",width=10,borderwidth=3, textvariable=var4, state=DISABLED)
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
path0=resource_path0("button.png")
buttonIMG=PhotoImage(file=path0)
datamoshbtn=Button(root,image=buttonIMG,borderwidth=0, highlightthickness=0, padx=0,pady=0,command=Step1)
datamoshbtn.place(x=100,y=270)
root.mainloop()
#DEVELOPER: AKASH BORA (a.k.a Akascape)
#Version=1.0
