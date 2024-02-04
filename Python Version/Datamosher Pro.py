"""
DATAMOSHER PRO Py version 2.2
Author: Akash Bora (Akascape)
License: MIT | Copyright (c) 2024 Akash Bora
"""

currentversion = 2.2

#Import installed modules
import tkinter
from tkinter import messagebox, filedialog
import customtkinter
import sys
import os
import imageio_ffmpeg
import subprocess
import imageio
import threading
import webbrowser
import requests
import time
import random
import warnings
from Assets.CTkRangeSlider import CTkRangeSlider
from PIL import Image, ImageTk

#Import the local datamosh library
from DatamoshLib.Tomato import tomato
from DatamoshLib.Original import classic, repeat, pymodes
from DatamoshLib.FFG_effects import basic_modes, external_script

# get full base path
def resource(relative_path):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

#Main Window size
WIDTH = 780
HEIGHT = 520

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme(random.choice(["blue","green","dark-blue"]))

root = customtkinter.CTk()
root.title("Datamosher Pro (python version)")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.bind("<1>", lambda event: event.widget.focus_set())
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

frame_left = customtkinter.CTkFrame(master=root, width=180, corner_radius=0)
frame_left.grid(row=0, column=0, sticky="nswe")

frame_right = customtkinter.CTkFrame(master=root)
frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

icopath = ImageTk.PhotoImage(file=resource(os.path.join("Assets","Icons","Program_icon.png")))
root.wm_iconbitmap()
root.iconphoto(False, icopath)

#Get FFMPEG path (using the imageio_ffmpeg plugin)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

#Effect List
modelist = sorted(["Bloom", "Invert", "Jiggle", "Overlap", "Pulse", "Reverse",
                   "Random", "Classic", "Glide", "Sort", "Echo", "Void",
                   "Fluid", "Stretch", "Motion Transfer", "Repeat", "Shear", "Delay", "Sink",
                   "Mirror", "Vibrate", "Slam Zoom", "Zoom","Invert-Reverse", "Shift",
                   "Noise", "Stop", "Buffer", "Slice", "Shuffle", "Rise", "Custom Script",
                   "Water Bloom", "Combine"])
current = modelist[0] 

#Making the top widgets for changing the modes dynamically
def ChangeModeRight():
    global current
    modelist.append(modelist.pop(0))
    current = modelist[0]
    mode_info.configure(text=current)
    dynamic()
    
def ChangeModeLeft():
    global current
    modelist.insert(0, modelist.pop())
    current = modelist[0]
    mode_info.configure(text=current)
    dynamic()
    
frame_info = customtkinter.CTkFrame(master=frame_right, width=520)
frame_info.pack(padx=10, pady=10, fill="x", anchor="n")

play_icon = Image.open(resource(os.path.join("Assets","Icons","right_icon.png"))).resize((20, 20), Image.Resampling.LANCZOS)

left_but = customtkinter.CTkButton(master=frame_info, image=customtkinter.CTkImage(play_icon.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                                   text="", width=50, height=50, corner_radius=10, fg_color=("white", "gray38"), hover_color=("gray90","gray25"),
                                   command=ChangeModeLeft)
left_but.pack(padx=10, pady=10, fill="x", side="left", anchor="n")

mode_info = customtkinter.CTkLabel(master=frame_info,text=current, corner_radius=10, width=320, height=50, fg_color=("white", "gray38"))
mode_info.pack(padx=10, pady=10, fill="x", expand=True, side="left", anchor="n")

right_but = customtkinter.CTkButton(master=frame_info, image=customtkinter.CTkImage(play_icon), text="", width=50, height=50,
                                   corner_radius=10, fg_color=("white", "gray38"), hover_color=("gray90","gray25"), command=ChangeModeRight)
right_but.pack(padx=10, pady=10, fill="x", side="right", anchor="n")

mode_type = customtkinter.CTkLabel(master=frame_right, text="")
mode_type.place(x=20, y=100)

#Open video function
previous = ""
ofile = ""
sfile = ""

def open_function(file=None):
    global ofile, vid_image2, previous, duration, vid
    
    if not file:
        ofile = filedialog.askopenfilename(filetypes=[('Video', ['*.mp4','*.avi','*.mov','*.mkv','*gif']),('All Files', '*.*')])
    else:
        ofile = file
    #Check the video type
    supported = ["mp4","avi","mov","gif","mkv","wmv","m4v"]
    
    if ofile:
        if ofile[-3:].lower() not in supported:
            print("This file type is not supported!")
            return
        previous = ofile
    else:
        ofile = previous
        return
    
    if len(os.path.basename(ofile))>=20:
        showinput=os.path.basename(ofile)[:10]+"..."+os.path.basename(ofile)[-3:]
    else:
        showinput=os.path.basename(ofile)[:20]
            
    #Change the thumbnail
    button_open.configure(fg_color='grey', text=showinput)
    outpng = resource(os.path.join("Assets","thumbnail_cache","vid_thumbnail.jpg"))
    button_thumbnail.configure(image=vid_image)
    if os.path.exists(outpng):
            os.remove(outpng)
    subprocess.call(f'"{ffmpeg}" -loglevel quiet -ss 00:00:01 -t 00:00:01 -i "{ofile}" -qscale:v 2 -r 10.0 "{outpng}"', shell=True)
    vid_image2 = customtkinter.CTkImage(Image.open(outpng), size=(170,100))
    button_thumbnail.configure(image=vid_image2)
    vid = imageio.get_reader(ofile, 'ffmpeg')
    
    #Update the widgets data
    position_frame.configure(to=vid.count_frames(), number_of_steps=vid.count_frames())
    duration = vid.get_meta_data()['duration']
    rangebar.configure(from_=0, to=int(duration), number_of_steps=int(duration))
    rangebar.set([0,duration])
    label_seconds2.configure(text="End: "+str(int(duration))+"s")
    rangebar2.configure(from_=1, to=vid.count_frames(), number_of_steps=vid.count_frames())
    rangebar2.set([0,vid.count_frames()])
    label_showframe2.configure(text="End: "+str(vid.count_frames()))
    shuf_slider.configure(to=vid.count_frames(), number_of_steps=vid.count_frames())
    end_mosh.set(duration)
    end_frame_mosh.set(vid.count_frames())
    position_frame.set(1)
    position_frame._command(position_frame.get())
    video_tbox.insert("end", ofile+"\n\n")

def reuse_video():
    if os.path.exists(sfile):
        open_function(file=sfile)
    else:
        messagebox.showinfo("No Output", "The moshed file is not found")
    button_reuse.place_forget()
    
#Left Frame Widgets
label_appname = customtkinter.CTkLabel(master=frame_left, text="DATAMOSHER PRO", font=("",14,"bold"))
label_appname.pack(pady=10, padx=5)

vid_image = customtkinter.CTkImage(Image.open(resource(os.path.join("Assets","thumbnail_cache","offline_image.png"))), size=(170,100))

button_thumbnail = customtkinter.CTkLabel(master=frame_left, image=vid_image, width=172, height=102, text="", bg_color="grey30")
button_thumbnail.pack(pady=0, padx=5)

add_video_image = customtkinter.CTkImage(Image.open(resource(os.path.join("Assets","Icons","video_icon.png"))), size=(20,15))

button_open = customtkinter.CTkButton(master=frame_left, image=add_video_image, text="IMPORT VIDEO", height=35,
                                      compound="right", command=open_function)
button_open.pack(pady=(20,5), padx=10, fill="x")

label_export = customtkinter.CTkLabel(master=frame_left,anchor="w",text="Export Format")
label_export.pack(padx=10, anchor="w")

optionmenu_1 = customtkinter.CTkComboBox(master=frame_left, height=35, values=["mp4","avi","mov","mkv"], state="readonly")
optionmenu_1.set("mp4")
optionmenu_1.pack(padx=10, fill="x")

up_arrow_image = customtkinter.CTkImage(Image.open(resource(os.path.join("Assets","Icons","up_arrow.png"))), size=(20,15))

button_reuse = customtkinter.CTkButton(master=frame_left, image=up_arrow_image, text="Import Moshed", height=35, width=160, fg_color="transparent",
                                      compound="right", command=reuse_video, border_width=2, text_color=["black", "white"])

#Info Window
def close_top():
    window_UI.destroy()
    info_setting.configure(state=tkinter.NORMAL)
    
def view_info():
    global window_UI
    window_UI = customtkinter.CTkToplevel(root)
    window_UI.geometry("410x200")
    window_UI.maxsize(410,200)
    window_UI.minsize(410,200)
    window_UI.title("About")
    window_UI.wm_iconbitmap()
    window_UI.after(300, lambda: window_UI.iconphoto(False, icopath))
    info_setting.configure(state=tkinter.DISABLED)
    window_UI.resizable(False, False)
    window_UI.wm_transient(root)
    
    def check():
        URL = "https://raw.githubusercontent.com/Akascape/Datamosher-Pro/Miscellaneous/VERSIONPY.txt"
        try:
            response = requests.get(URL)
            new_version = float(response.content)
        except:
            messagebox.showinfo("Unable to connect!",
                                "Unable to get information, please check your internet connection or visit the github repository.")
            return
        time.sleep(1)
        
        if new_version>currentversion:
            messagebox.showinfo("New Version available!","A new version "+ str(new_version) +
                                " is available, \nPlease visit the github repository or the original download page!")
        else:
            messagebox.showinfo("No Updates!", "You are on the latest version!")
                
    def docs():
        webbrowser.open_new_tab("https://github.com/Akascape/Datamosher-Pro/wiki")
        
    def repo():
        webbrowser.open_new_tab("https://github.com/Akascape/Datamosher-Pro/issues")
        
    logo = customtkinter.CTkLabel(master=window_UI, image=logo_image, text="",
                                  bg_color=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
    logo.place(x=200,y=0)
    
    visit = customtkinter.CTkButton(window_UI, text="Report Bug", width=150, height=35, corner_radius=10, command=repo)
    visit.place(x=20,y=30)
    
    checkupdate = customtkinter.CTkButton(window_UI, text="Check For Updates", width=150, height=35, corner_radius=10, command=check)
    checkupdate.place(x=20,y=80)
    
    helpbutton = customtkinter.CTkButton(window_UI, text="Help", width=150, height=35, corner_radius=10,command=docs)
    helpbutton.place(x=20,y=130)
    
    version_label = customtkinter.CTkLabel(window_UI,anchor="w",width=1, text="v"+str(currentversion),
                                           fg_color=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
    version_label.place(x=365, y=2)
    
    dvname = customtkinter.CTkLabel(window_UI,anchor="w",width=1, text="Developer: Akash Bora")
    dvname.place(x=30,y=170)
    
    window_UI.protocol("WM_DELETE_WINDOW", close_top)

logo_image = customtkinter.CTkImage(Image.open(resource(os.path.join("Assets","Icons","Logo.png"))), size=(210,200))

infopng = customtkinter.CTkImage(Image.open(resource(os.path.join("Assets","Icons","info.png"))).resize((20, 20), Image.Resampling.LANCZOS))

info_setting = customtkinter.CTkButton(master=frame_left, image=infopng, text="", width=40, height=40, corner_radius=10,
                                       fg_color=customtkinter.ThemeManager.theme["CTkButton"]["text_color_disabled"],
                                       hover_color=("grey50","gray25"), command=view_info)
info_setting.pack(padx=10, pady=10, anchor="s", side="left")

def close_top2():
    window_UI2.destroy()
    ff_setting.configure(state=tkinter.NORMAL)
    
def change_param():
    global window_UI2
    
    def set_param():
        global param
        param = text_box.get("0.0", tkinter.END)
        if len(param)==1:
            param = ""
        close_top2()
        
    window_UI2 = customtkinter.CTkToplevel(root)
    window_UI2.geometry("410x200")
    window_UI2.maxsize(410,200)
    window_UI2.minsize(410,200)
    window_UI2.title("Custom FFmpeg Parameters")
    window_UI2.wm_iconbitmap()
    window_UI2.resizable(False, False)
    window_UI2.after(300, lambda: window_UI2.iconphoto(False, icopath))
    ff_setting.configure(state=tkinter.DISABLED)
    window_UI2.wm_transient(root)

    text_box = customtkinter.CTkTextbox(window_UI2, border_width=3, height=140, undo=True)
    text_box.pack(padx=10, pady=(10,0), fill="x")
    if len(param)>1: text_box.insert("0.0", param)
    ok_button = customtkinter.CTkButton(window_UI2, text="OK", command=set_param)
    ok_button.pack(padx=10, pady=10, fill="x")
    
    window_UI2.protocol("WM_DELETE_WINDOW", close_top2)
    
settingpng = customtkinter.CTkImage(Image.open(resource(os.path.join("Assets","Icons","settings.png"))).resize((20, 20), Image.Resampling.LANCZOS))

ff_setting = customtkinter.CTkButton(master=frame_left, image=settingpng, text="", width=40, height=40, corner_radius=10,
                                    fg_color=customtkinter.ThemeManager.theme["CTkButton"]["text_color_disabled"],
                                    hover_color=("grey50","gray25"), command=change_param)
ff_setting.pack(padx=(65,10), pady=10, anchor="s", side="right")

#Validation for entries
def only_numbers(char):
    if ((char.isdigit()) or (char=="")) and (len(char)<=6):
        return True
    else:
        return False
validation = root.register(only_numbers)

### Dynamimc widgets that change with modes ###

widget_frame = customtkinter.CTkFrame(master=frame_right, fg_color="transparent")
widget_frame.pack(padx=10, pady=(50,10), expand=True, fill="both")

widget_frame.columnconfigure((0,1,2,3), weight=1)
widget_frame.rowconfigure(5, weight=1)

#Kill Frame Widget
    
label_kill = customtkinter.CTkLabel(master=widget_frame,anchor="w",text="Kill Frame Size: 0.6")
slider_kill = customtkinter.CTkSlider(master=widget_frame, from_=1, to=0, number_of_steps=100,
                                      command=lambda value: label_kill.configure(text="Kill Frame Size: "+str(round(value,4))))
slider_kill.set(0.6)

#N-frameWidget
varn = tkinter.StringVar()
label_ctime = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Frame Count:",width=1)
ctime = customtkinter.CTkEntry(widget_frame,textvariable=varn, validate='key', validatecommand=(validation, '%P'), placeholder_text="1",
                             width=100, placeholder_text_color="grey70", height=30, border_width=2, corner_radius=10)
varn.set(1)

#Keep frame & Keep audio widgets
keepaudio = customtkinter.CTkCheckBox(master=widget_frame, text="Keep Audio", onvalue=1, offvalue=0)
keepframe = customtkinter.CTkCheckBox(master=widget_frame, text="Keep First Frame", onvalue=1, offvalue=0)

#Count Frame widget
label_frame1 = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Position Frame: 1",width=1)

position_frame = customtkinter.CTkSlider(master=widget_frame, progress_color="black", fg_color="black", from_=1, to=1.1, number_of_steps=1,
                                         command=lambda value: label_frame1.configure(text="Position Frame: "+str(int(value))))
position_frame.set(1)

#Classic Rangebar
start_mosh = tkinter.DoubleVar(value=0)
end_mosh = tkinter.DoubleVar(value=1)

rangebar = CTkRangeSlider(widget_frame, variables=[start_mosh, end_mosh], number_of_steps=1)

label_seconds1 = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Start: 0s",width=1)
label_seconds2 = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="End: 0s",width=1)
label_segment = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Choose Segment:",width=1)

def show2(*args):
        if previous=="":
            return
        label_seconds2.configure(text="End: "+str(int(end_mosh.get()))+"s")
        
def show(*args):
        if previous=="":
            return
        label_seconds1.configure(text="Start: "+str(int(start_mosh.get()))+"s")
        
start_mosh.trace_add('write', show)
end_mosh.trace_add('write', show2)

#Delta entry widget
label_p = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="P-frames (Delta):",width=1)
label_segment = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Choose Segment:",width=1)

varp = tkinter.StringVar()
delta = customtkinter.CTkEntry(widget_frame, placeholder_text="1",validate='key', validatecommand=(validation, '%P'),
                               width=100, textvariable=varp, placeholder_text_color="grey70", height=30, border_width=2,
                               corner_radius=10)
varp.set(1)

#Frame Rangebar for repeat and rise modes
start_frame_mosh = tkinter.DoubleVar(value=0)
end_frame_mosh = tkinter.DoubleVar(value=1)

rangebar2 = CTkRangeSlider(widget_frame, variables=[start_frame_mosh, end_frame_mosh], number_of_steps=1)

label_showframe1 = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Start Frame: 0",width=1)
label_showframe2 = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="End: 0",width=1)
label_segment2 = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Choose Frame Segment:",width=1)

def show3(*args):
        if previous=="":
            return
        label_showframe2.configure(text="End: "+str(int(end_frame_mosh.get())))
        
def show4(*args):
        if previous=="":
            return
        label_showframe1.configure(text="Start Frame: "+str(int(start_frame_mosh.get())))
        
start_frame_mosh.trace_add('write', show4)
end_frame_mosh.trace_add('write', show3)

#slider for echo mode
    
label_mid = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Start Point: 0.5",width=1)
mid_point = customtkinter.CTkSlider(master=widget_frame, progress_color="black", fg_color="black",
                                    from_=0, to=1, number_of_steps=10,
                                    command=lambda value: label_mid.configure(text="Start Point: "+str(round(value,1))))
mid_point.set(0.5)

#Some options for sort mode
keepsort = customtkinter.CTkCheckBox(master=widget_frame, text="Keep First Frames", onvalue=0, offvalue=1)
reversesort = customtkinter.CTkCheckBox(master=widget_frame, text="Reverse", onvalue=False, offvalue=True)

#Options for ffglitch modes
hw_auto = customtkinter.CTkSwitch(master=widget_frame,text="HW Acceleration \n(Auto)",onvalue=1, offvalue=0)
labelk = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Keyframes:",width=1)
kf = customtkinter.CTkComboBox(master=widget_frame,height=30, width=150, values=["1000", "100", "10", "1"])
kf._entry.config(validate='key', validatecommand=(validation, '%P'))

#Widget for Shuffle mode 
shuf_label = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Chunk Size: 1",width=1)
shuf_slider = customtkinter.CTkSlider(master=widget_frame, from_=1, to=0, number_of_steps=1,
                                      command=lambda value:shuf_label.configure(text="Chunk Size: "+str(int(value))))
shuf_slider.set(1)

#Widget for Fluid mode
fluid_label = customtkinter.CTkLabel(master=widget_frame,anchor='w',text="Amount: 5",width=1)
slider_fluid = customtkinter.CTkSlider(master=widget_frame, width=500, from_=1, to=20, number_of_steps=100,
                                       command=lambda value:fluid_label.configure(text="Amount: "+str(int(value))))
slider_fluid.set(5)

#Stretch mode widget
v_h = customtkinter.CTkSwitch(widget_frame,text="Horizontal Stretch", onvalue=1, offvalue=0)

#Button for motion transfer mode
def open_MT():
    global vfile
    vfile = filedialog.askopenfilename(filetypes=[('Vector File', ['*.mp4','*.avi','*.mov','*.mkv']),('All Files', '*.*')])
    if vfile:
        mt_button.configure(fg_color='grey', text=os.path.basename(vfile))
    else:
        mt_button.configure(fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"], text="OPEN VIDEO")
        vfile = ''
    
mt_button = customtkinter.CTkButton(master=widget_frame, text="OPEN VIDEO", height=30, compound="right",command=open_MT)

#Button for custom script mode
scriptfile = ''

def open_script():
    global scriptfile
    scriptfile = filedialog.askopenfilename(filetypes=[('Script File', ['*.js','*.py']),('All Files', '*.*')])
    if scriptfile:
        scriptbutton.configure(fg_color='grey', text=os.path.basename(scriptfile))
    else:
        scriptbutton.configure(fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"], text='OPEN SCRIPT')
        scriptfile = ''
        
scriptbutton = customtkinter.CTkButton(master=widget_frame, text="OPEN SCRIPT", height=30, compound="right",command=open_script)

#Combine mode widgets

def open_multiple_videos():
    files = filedialog.askopenfilenames(filetypes=[('Vector File', ['*.mp4','*.avi','*.mov','*.mkv']),('All Files', '*.*')])
    if files:
        supported = ["mp4","avi","mov","gif","mkv","wmv","m4v"]
        for i in files:
            if i[-3:].lower() in supported:
                video_tbox.insert("end", i+"\n\n")
    
import_bt = customtkinter.CTkButton(master=widget_frame, text="Add Videos", fg_color="transparent", border_width=2,
                                    command=open_multiple_videos, text_color=["black", "white"])
video_tbox = customtkinter.CTkTextbox(master=widget_frame, undo=True)

#Dynamic UI functions for each widget
def rangeslider(x):
    if x==1:
        rangebar.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5)
        label_seconds1.grid(row=1, column=0, sticky="w", padx=10)
        label_seconds2.grid(row=1, column=3, sticky="e", padx=10)
        label_segment.grid(row=0, column=0, sticky="w", padx=10)
    else:
        rangebar.grid_forget()
        label_segment.grid_forget()
        label_seconds1.grid_forget()
        label_seconds2.grid_forget()
        
def rangeslider2(x):
    if x==1:
        if (current=="Rise"):
            rangebar2.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5)
            label_showframe1.grid(row=2, column=0, sticky="w", padx=10)
            label_showframe2.grid(row=2, column=3, sticky="e", padx=10)
            label_segment2.grid(row=1, column=0, sticky="w", padx=10, pady=(10,0))
        else:
            rangebar2.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5)
            label_showframe1.grid(row=1, column=0, sticky="w", padx=10)
            label_showframe2.grid(row=1, column=3, sticky="e", padx=10)
            label_segment2.grid(row=0, column=0, sticky="w", padx=10)
    else:
        rangebar2.grid_forget()
        label_showframe1.grid_forget()
        label_showframe2.grid_forget()
        label_segment2.grid_forget()
        
def mid(x):
    if x==1:
        mid_point.grid(row=1, columnspan=4, padx=10, sticky="ew")
        label_mid.grid(row=0, padx=15, sticky="w")
    else:
        mid_point.grid_forget()
        label_mid.grid_forget()
        
def killoption(x):
    if x==1 or x==2 or x==3:
        label_kill.grid(row=0, column=0, sticky="w", padx=10)
        slider_kill.grid(row=1, column=0, columnspan=4, padx=5, sticky="ew")
    else:
        label_kill.grid_forget()
        slider_kill.grid_forget()
        
def positionslider(x):
    if x==1:
        label_frame1.grid(row=2, column=0, sticky="w", padx=10, pady=(10,0))
        position_frame.grid(row=3, column=0, columnspan=4, padx=5, sticky="ew")
    else:
        label_frame1.grid_forget()
        position_frame.grid_forget()
        
def framekeep(x):
    if x==1:
        keepframe.grid(row=4, column=2, sticky="e", padx=10, pady=15)
    elif x==2:
        keepframe.grid(row=4, column=2, sticky="e", padx=10, pady=15)
    else:
        keepframe.grid_forget()
        
def audiokeep(x):
    if x==1:     
        keepaudio.grid(row=4, column=3, sticky="e", padx=10, pady=15)
    elif x==2:
        keepaudio.grid(row=4, column=3, sticky="e", padx=10, pady=15)
    else:
        keepaudio.grid_forget()
        
def ctimes(x):
    if x==1:
        ctime.grid(row=4, column=0, sticky="w", padx=(100,10), pady=10)
        label_ctime.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        if current=="Water Bloom":
            varn.set(20)
        else:
            varn.set(1)
    else:
        ctime.grid_forget()
        label_ctime.grid_forget()
        
def pdelta(x):
    if x==1:
        delta.grid(row=3, column=0, sticky="w", padx=(120,10), pady=10)
        label_p.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        if current=="Repeat":
            varp.set(5)
    elif x==2:
        delta.grid(row=3, column=0, sticky="w", padx=(120,10), pady=10)
        label_p.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        if current=="Glide":
            varp.set(5)
    else:
        delta.grid_forget()
        label_p.grid_forget()
        
def sortoptions(x):
    if x==1:
        keepsort.grid(row=0, column=0,sticky="w", padx=10)
        reversesort.grid(row=0, column=1,sticky="w", padx=10)
    else:
        keepsort.grid_forget()
        reversesort.grid_forget()
        
def ffgassist(x):
    if x==1:
        hw_auto.grid(row=0, column=0, sticky="w", padx=10)
        labelk.grid(row=0, column=3, sticky="e", padx=(10,170))
        kf.grid(row=0, column=3, sticky="e", padx=10)
    else:
        hw_auto.grid_forget()
        labelk.grid_forget()
        kf.grid_forget()
        
def shuf(x):
    if x==1:
        shuf_label.grid(row=1, column=0, sticky="w", padx=10, pady=(15,0))
        shuf_slider.grid(row=2, column=0, sticky="ew", columnspan=4, padx=5)
    else:
        shuf_label.grid_forget()
        shuf_slider.grid_forget()
        
def fluidwidget(x):
    if x==1:
        fluid_label.grid(row=1, column=0, sticky="w", padx=10, pady=(15,0))
        slider_fluid.grid(row=2, column=0, sticky="ew", columnspan=4, padx=5)
    else:
        fluid_label.grid_forget()
        slider_fluid.grid_forget()
        
def h_v(x):
    if x==1:
        v_h.grid(sticky="w", pady=15, padx=10)
    else:
        v_h.grid_forget()
        
def mtwid(x):
    if x==1:
        mt_button.grid(row=1, columnspan=4, sticky="ew", padx=10, pady=20)
    else:
        mt_button.grid_forget()

def cbwidget(x):
    if x==1:
        import_bt.grid(row=1, column=0, columnspan=4, sticky="we", padx=10, pady=10)
        video_tbox.grid(row=5, column=0, columnspan=4, rowspan=3, sticky="news", padx=10)
    else:
        import_bt.grid_forget()
        video_tbox.grid_forget()
        
def custom(x):
    if x==1:
        scriptbutton.grid(row=1, columnspan=4, sticky="ew", padx=10, pady=20)
    else:
        scriptbutton.grid_forget()

#Main function to update the widgets
def dynamic():
    global current, showwidgets
    allwidgets = [audiokeep, positionslider, killoption, framekeep,
                ctimes, pdelta, rangeslider, rangeslider2, mid,
                  sortoptions, ffgassist, fluidwidget, h_v, custom,
                  mtwid, shuf, cbwidget]
    
    for i in allwidgets:
        i(0)
        
    showwidgets = []
    if (current=="Bloom") or  (current=="Pulse") or (current=="Pulse") or(current=="Overlap"):
        showwidgets=[audiokeep, positionslider, killoption, framekeep, ctimes]
        u=1
        mode_type.configure(text="Mode Type: Automosh (Tomato)")
        
    elif (current=="Jiggle"):
        showwidgets=[positionslider, audiokeep, killoption, framekeep]
        u=1
        mode_type.configure(text="Mode Type: Automosh (Tomato)")
        
    elif (current=="Void") or (current=="Reverse") or (current=="Invert") or (current=="Random"):
        showwidgets=[killoption,audiokeep, framekeep]
        u=2
        mode_type.configure(text="Mode Type: Automosh (Tomato)")
        
    elif (current=="Classic"):
        showwidgets=[rangeslider, pdelta]
        u=1
        mode_type.configure(text="Mode Type: FFmpeg")
        
    elif (current=="Glide"):
        showwidgets=[pdelta]
        u=2
        mode_type.configure(text="Mode Type: FFmpeg")
        
    elif (current=="Repeat") or (current=="Rise"):
        if (current=="Rise"): 
            showwidgets=[rangeslider2, ffgassist]
        else:
            showwidgets=[rangeslider2, pdelta]
        u=1
        mode_type.configure(text="Mode Type: FFmpeg")
        
    elif (current=="Echo"):
        showwidgets=[mid]
        u=1
        mode_type.configure(text="Mode Type: FFmpeg")
        
    elif (current=="Sort"):
        showwidgets=[sortoptions]
        u=1
        mode_type.configure(text="Mode Type: FFmpeg")
        
    elif ((current=="Buffer") or (current=="Sink") or (current=="Mirror") or (current=="Shear") or (current=="Noise")
         or (current=="Delay") or (current=="Slam Zoom") or (current=="Invert-Reverse") or (current=="Shift") or (current=="Zoom")
         or (current=="Slice")or (current=="Vibrate") or (current=="Stop")):
        showwidgets=[ffgassist]
        u=1
        mode_type.configure(text="Mode Type: FFglitch")
        
    elif (current=="Fluid"):
        showwidgets=[ffgassist, fluidwidget]
        u=1
        mode_type.configure(text="Mode Type: FFglitch")
        
    elif (current=="Stretch"):
        showwidgets=[ffgassist, h_v]
        u=1
        mode_type.configure(text="Mode Type: FFglitch")
        
    elif (current=="Motion Transfer"):
        showwidgets=[ffgassist, mtwid]
        u=1
        mode_type.configure(text="Mode Type: FFglitch")
        
    elif (current=="Custom Script"):
        showwidgets=[ffgassist, custom]
        u=1
        mode_type.configure(text="Mode Type: FFglitch")
        
    elif (current=="Shuffle"):
        showwidgets=[ffgassist, shuf]
        u=1
        mode_type.configure(text="Mode Type: FFglitch")
        
    elif (current=="Combine"):
        showwidgets=[ffgassist, cbwidget]
        u=1
        mode_type.configure(text="Mode Type: FFglitch")
        
    elif (current=="Water Bloom"):
        showwidgets=[ffgassist, positionslider, ctimes]
        u=1
        mode_type.configure(text="Mode Type: FFglitch")
        
    for widgets in showwidgets:
            widgets(u)
            
dynamic()
keepframe.select()
param = ""

#autosave video name
def savename():
    global sfile
    if ofile:
        try:
            if str(ofile).find("_datamoshed_")>0:
                extra_keyword = "_"
            else:
                extra_keyword = "_datamoshed_"
            sfile = ofile[:-4]+extra_keyword+current+'.'+optionmenu_1.get()
            nf = 0
            while os.path.exists(sfile):
                nf = nf+1
                sfile = ofile[:-4]+extra_keyword+current+'('+str(nf)+')'+'.'+optionmenu_1.get()
        except:
            sfile = ""
            
#function that will thread the main process
def Threadthis():
    global varp, varn
    if delta.get()=='' or delta.get()<'1':
        varp.set(1)
    if ctime.get()=='' or ctime.get()<'1':
        varn.set(1)
    threading.Thread(target=do_the_mosh).start()
    
#Converter function
def ffmpeg_convert(inputpath, parameters, outputpath, extra=''):
    subprocess.call(f'"{ffmpeg}" {extra} -i "{inputpath}" {parameters} -y "{outputpath}"', shell=True)

#Main function of the whole program
def do_the_mosh():
    global ofile, sfile, param
    last_used = current
    if previous=="":
        messagebox.showinfo("No Video imported!","Please import a video file!")
        return
    button_mosh.configure(state=tkinter.DISABLED)
    button_open.configure(state=tkinter.DISABLED)
    try:
        savename()
        ProcessLabel.configure(text='STEP 1/3 CONVERTING...')
        if param=="":         
            param = "-c:v libx264 -preset medium -b:v 2M -minrate 2M -maxrate 2M -bufsize 2M" # Default ffmpeg parameter
            changed = False
        else:
            changed = True
        if ((current=="Bloom") or  (current=="Pulse") or (current=="Pulse") or(current=="Overlap")
            or (current=="Void") or (current=="Reverse") or (current=="Invert") or (current=="Random") or (current=="Jiggle")):
            ifile = sfile[:-4]+".avi"
            ffmpeg_convert(ofile,param,ifile)
            ProcessLabel.configure(text='STEP 2/3 MOSHING...')
            mfile = sfile[:-4]+"_corrupted.avi"
            tomato.mosh(infile=ifile, outfile=mfile, m=current.lower(), c=int(varn.get()), n=int(position_frame.get()),
                        k=round(slider_kill.get(),4), a=keepaudio.get(), f=keepframe.get())
            time.sleep(1)
            os.remove(ifile)
            ProcessLabel.configure(text='STEP 3/3 FIXING THE CORRUPTED FILE...')
            ffmpeg_convert(mfile,param,sfile)
            os.remove(mfile)
        elif ((current=="Classic") or (current=="Repeat") or (current=="Glide") or (current=="Sort") or (current=="Echo")):
            if not changed:
                param = "-bf 0 -b 10000k" # Default ffmpeg parameter for the above modes
            ifile = sfile[:-4]+".avi"
            ffmpeg_convert(ofile,param,ifile)
            ProcessLabel.configure(text='STEP 2/3 MOSHING...')
            mfile = sfile[:-4]+"_corrupted.avi"
            if current=="Classic":
                classic.Datamosh(ifile, mfile,s=int(start_mosh.get()),e=int(end_mosh.get()),p=int(varp.get()), fps=vid.get_meta_data()['fps'])
            elif current=="Repeat":         
                repeat.Datamosh(ifile, mfile, s=int(start_frame_mosh.get()), e=int(end_frame_mosh.get()),
                                p=int(varp.get()), fps=vid.get_meta_data()['fps'])
            elif current=="Glide":
                pymodes.library.glide(int(varp.get()), ifile, mfile)
            elif current=="Sort":
                pymodes.library.avi_sort(ifile, mfile, mode=keepsort.get(), rev=reversesort.get())
            elif current=="Echo":
                pymodes.library.process_streams(ifile, mfile, mid=round(mid_point.get(),1))
            os.remove(ifile)
            ProcessLabel.configure(text='STEP 3/3 FIXING THE CORRUPTED FILE...')
            ffmpeg_convert(mfile,param,sfile)
            os.remove(mfile)
        else:
            time.sleep(1)
            ProcessLabel.configure(text='STEP 2/3 MOSHING...')
            mfile = sfile[:-4]+"_corrupted.mpg"
            if current=="Fluid":
                basic_modes.library(ofile, mfile, mode=3, fluidity=int(slider_fluid.get()), gop=kf.get())
            elif current=="Stretch":
                basic_modes.library(ofile, mfile, mode=2, vh=v_h.get(), gop=kf.get())
            elif current=="Motion Transfer":
                if vfile:
                    basic_modes.library(ofile, mfile, mode=1, extract_from=vfile, gop=kf.get())
                else:
                    messagebox.showinfo("No Vector File imported!", "Please choose the video from where you want to extract the vector motion.")
                    button_mosh.configure(state=tkinter.NORMAL)
                    button_open.configure(state=tkinter.NORMAL)
                    ProcessLabel.configure(text='Choose any secondary video file for transfering the vectors!')
                    return
            elif current=="Shuffle":
                basic_modes.library(ofile, mfile, mode=4, size=int(shuf_slider.get()), gop=kf.get())
            elif current=="Rise":
                basic_modes.library(ofile, mfile, mode=5, s=int(start_frame_mosh.get()),
                                    e=int(end_frame_mosh.get()-start_frame_mosh.get()), gop=kf.get())
            elif current=="Water Bloom":
                basic_modes.library(ofile, mfile, mode=6, f=int(position_frame.get()), r=int(varn.get()), gop=kf.get())
            elif current=="Combine":
                all_files = video_tbox.get('1.0', 'end').split('\n')
                real_files = []
                for i in all_files:
                    if os.path.isfile(i):
                        real_files.append(i)
                if len(real_files)<=1:
                    messagebox.showinfo("No files added", "Please import 2 or more videos to use combine mode!")
                    button_mosh.configure(state=tkinter.NORMAL)
                    button_open.configure(state=tkinter.NORMAL)
                    ProcessLabel.configure(text='Add 2 or more videos in combine mode!')
                    return
                basic_modes.library(real_files, mfile, mode=7, gop=kf.get())
            elif current=="Custom Script":
                external_script.mosh(ofile, mfile, mode=1, scriptfile=scriptfile, gop=kf.get())
            else:
                external_script.mosh(ofile, mfile, mode=2, effect=current, gop=kf.get())
            ProcessLabel.configure(text='STEP 3/3 FIXING THE CORRUPTED FILE...')
            if hw_auto.get()==1:
                hw_type=' -hwaccel auto '
            else:
                hw_type=''
            ffmpeg_convert(mfile,param,sfile,extra=hw_type)
            os.remove(mfile)
        if not changed:
            param=""
    except Exception as errors:
        warnings.warn(str(errors))
    
    #Check the result and complete the task
    if os.path.exists(sfile):
        messagebox.showinfo("Exported!", "File exported successfully, \nFile Location: " +str(sfile))
        ProcessLabel.configure(text="Last used: "+last_used)
        try: os.startfile(sfile)
        except: pass
    else:
        messagebox.showerror("Oops!", "Something went wrong! \nPlease recheck the settings and try again.")
        ProcessLabel.configure(text='Recheck the settings and try again!')
        
    button_open.configure(state=tkinter.NORMAL)
    button_mosh.configure(state=tkinter.NORMAL)
    button_reuse.place(x=10, y=290)
    
#Bottom Widgets
ProcessLabel = customtkinter.CTkLabel(master=frame_right, width=400, height=30,corner_radius=10,
                                      text="START DATAMOSHING!", fg_color=("white", "gray38"))
ProcessLabel.pack(padx=10, pady=10, fill="x", expand=True, side="left")

button_mosh = customtkinter.CTkButton(master=frame_right, height=30,width=110,corner_radius=10,
                                      text="MOSH", command=Threadthis)
button_mosh.pack(padx=(0,10), pady=10, fill="x", side="right")

root.mainloop()

#--------------------------------------------------------------------#
