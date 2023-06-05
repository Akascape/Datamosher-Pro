#Author: Akash Bora
#License: MIT | Copyright (c) 2023 Akash Bora

currentversion = 2.01

#Import required modules
import tkinter
import customtkinter
import sys
import os
import imageio_ffmpeg
import subprocess
import imageio
from PIL import Image, ImageTk
from RangeSlider.RangeSlider import RangeSliderH
import threading
import webbrowser
import requests
import time
import random
import warnings

#Import the local datamosh library
from DatamoshLib.Tomato import tomato
from DatamoshLib.Original import classic, repeat, pymodes
from DatamoshLib.FFG_effects import basic_modes, external_script

#Get base path
def resource(relative_path):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

#Main Window size
WIDTH = 780
HEIGHT = 520

if sys.platform.startswith("win"):
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(0)
    except:
        pass
    
customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme(random.choice(["blue","green","dark-blue"]))
root = customtkinter.CTk()
root.title("Datamosher Pro (python version)")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.bind("<1>", lambda event: event.widget.focus_set())
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.resizable(width=False, height=False)
frame_left = customtkinter.CTkFrame(master=root,width=180,corner_radius=0)
frame_left.grid(row=0, column=0, sticky="nswe")
frame_right = customtkinter.CTkFrame(master=root)
frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
icopath = ImageTk.PhotoImage(file=resource(os.path.join("Assets","Icons","Program_icon.png")))
root.wm_iconbitmap()
root.iconphoto(False, icopath)

#get FFMPEG path (using the imageio_ffmpeg plugin)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

#Effect List
modelist = sorted(["Bloom", "Invert", "Jiggle", "Overlap", "Pulse", "Reverse",
       "Random", "Classic", "Glide", "Sort", "Echo", "Void",
       "Fluid", "Stretch", "Motion Transfer", "Repeat", "Shear", "Delay", "Sink",
       "Mirror", "Vibrate", "Slam Zoom", "Zoom","Invert-Reverse", "Shift",
       "Noise", "Stop", "Buffer", "Slice", "Shuffle", "Rise", "Custom Script", "Water Bloom"])
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
    
frame_info = customtkinter.CTkFrame(master=frame_right, width=520, height=100)
frame_info.pack(padx=10, pady=10, fill="x", expand=True, anchor="n")

play_icon = Image.open(resource(os.path.join("Assets","Icons","right_icon.png"))).resize((20, 20), Image.Resampling.LANCZOS)

left_but = customtkinter.CTkButton(master=frame_info, image=customtkinter.CTkImage(play_icon.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                                   text="", width=50, height=50, corner_radius=10, fg_color=("white", "gray38"), hover_color=("gray90","gray25"), command=ChangeModeLeft)
left_but.pack(padx=10, pady=10, fill="x", side="left", anchor="n")

mode_info = customtkinter.CTkLabel(master=frame_info,text=current, corner_radius=10, width=320, height=50, fg_color=("white", "gray38"))
mode_info.pack(padx=10, pady=10, fill="x", expand=True, side="left", anchor="n")

right_but = customtkinter.CTkButton(master=frame_info, image=customtkinter.CTkImage(play_icon), text="", width=50, height=50,
                                   corner_radius=10, fg_color=("white", "gray38"), hover_color=("gray90","gray25"), command=ChangeModeRight)
right_but.pack(padx=10, pady=10, fill="x", side="right", anchor="n")

#Open video function
previous = ""

def open_function():
    global ofile, vid_image2, previous, duration, vid
    
    ofile = tkinter.filedialog.askopenfilename(filetypes =[('Video', ['*.mp4','*.avi','*.mov','*.mkv','*gif']),('All Files', '*.*')])
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
    rangebar.max_val = duration
    label_seconds2.configure(text="End: "+str(int(duration))+"s")
    rangebar2.max_val = vid.count_frames()
    label_showframe2.configure(text="End: "+str(vid.count_frames()))
    shuf_slider.configure(to=vid.count_frames(), number_of_steps=vid.count_frames())
    end_mosh.set(duration)
    end_frame_mosh.set(vid.count_frames())
    
#Left Frame Widgets
label_appname = customtkinter.CTkLabel(master=frame_left, text="DATAMOSHER PRO")
label_appname.place(x=35,y=10)

vid_image = customtkinter.CTkImage(Image.open(resource(os.path.join("Assets","thumbnail_cache","offline_image.png"))), size=(170,100))

button_thumbnail = customtkinter.CTkLabel(master=frame_left, image=vid_image, width=172, height=102, text="", bg_color="grey30")
button_thumbnail.place(x=5,y=40)

add_video_image = customtkinter.CTkImage(Image.open(resource(os.path.join("Assets","Icons","video_icon.png"))), size=(20,15))

button_open = customtkinter.CTkButton(master=frame_left, image=add_video_image, text="IMPORT VIDEO", width=160, height=35,
                                      compound="right", command=open_function)
button_open.place(x=10,y=165)

label_export = customtkinter.CTkLabel(master=frame_left,anchor="w",text="Export Format")
label_export.place(x=12,y=205)

optionmenu_1 = customtkinter.CTkComboBox(master=frame_left, width=160, height=35, values=["mp4","avi","mov","mkv"], state="readonly")
optionmenu_1.set("mp4")
optionmenu_1.place(x=10,y=235)

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
            open(resource(os.path.join("Assets","version","VERSIONPY.txt")), "wb").write(response.content)
        except:
            tkinter.messagebox.showinfo("Unable to connect!", "Unable to get information, please check your internet connection or visit the github repository.")
            return
        time.sleep(1)
        
        with open(resource(os.path.join("Assets","version","VERSIONPY.txt")), 'r') as uf:
            nver=float(uf.read())
            if nver>currentversion:
                tkinter.messagebox.showinfo("New Version available!","A new version "+ str(nver) +
                                            " is available, \nPlease visit the github repository or the original download page!")
            else:
                tkinter.messagebox.showinfo("No Updates!", "You are on the latest version!")
                
    def docs():
        webbrowser.open_new_tab("https://github.com/Akascape/Datamosher-Pro/wiki")
        
    def repo():
        webbrowser.open_new_tab("https://github.com/Akascape/Datamosher-Pro/issues")
        
    logo_image = customtkinter.CTkImage(Image.open(resource(os.path.join("Assets","Icons","Logo.png"))), size=(210,200))
    logo = customtkinter.CTkLabel(master=window_UI, image=logo_image, text="",
                                  bg_color=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
    logo.place(x=200,y=0)
    
    visit = customtkinter.CTkButton(window_UI, text="Report Bug", width=150, height=35, corner_radius=10, command=repo)
    visit.place(x=20,y=30)
    
    checkupdate = customtkinter.CTkButton(window_UI, text="Check For Updates", width=150, height=35, corner_radius=10, command=check)
    checkupdate.place(x=20,y=80)
    
    helpbutton=customtkinter.CTkButton(window_UI, text="Help", width=150, height=35, corner_radius=10,command=docs)
    helpbutton.place(x=20,y=130)
    
    version_label = customtkinter.CTkLabel(window_UI,anchor="w",width=1, text="v"+str(currentversion),
                                           fg_color=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
    version_label.place(x=365, y=2)
    
    dvname = customtkinter.CTkLabel(window_UI,anchor="w",width=1, text="Developer: Akash Bora")
    dvname.place(x=30,y=170)
    
    window_UI.protocol("WM_DELETE_WINDOW", close_top)

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

    text_box = customtkinter.CTkTextbox(window_UI2, border_width=3,height=140)
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

#Kill Frame Widget
    
label_kill = customtkinter.CTkLabel(master=frame_right,anchor="w",text="Kill Frame Size: 0.6")
slider_kill = customtkinter.CTkSlider(master=frame_right, width=500, from_=1, to=0, number_of_steps=100,
                                      command=lambda value: label_kill.configure(text="Kill Frame Size: "+str(round(value,4))))
slider_kill.set(0.6)

#N-frameWidget
varn = tkinter.IntVar()
label_ctime = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Frame Count:",width=1)
ctime = customtkinter.CTkEntry(frame_right,textvariable=varn, validate='key', validatecommand=(validation, '%P'), placeholder_text="1",
                             width=100, placeholder_text_color="grey70", height=30, border_width=2, corner_radius=10)
varn.set(1)

#Keep frame & Keep audio widgets
keepaudio = customtkinter.CTkCheckBox(master=frame_right, text="Keep Audio", onvalue=1, offvalue=0)
keepframe = customtkinter.CTkCheckBox(master=frame_right, text="Keep First Frame", onvalue=1, offvalue=0)

#Count Frame widget
label_frame1 = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Position Frame: 1",width=1)

position_frame = customtkinter.CTkSlider(master=frame_right, width=500,progress_color="black", fg_color="black", from_=1, to=1.1,
                                         number_of_steps=1, command=lambda value: label_frame1.configure(text="Position Frame: "+str(int(value))))
position_frame.set(1)

#Classic Rangebar
start_mosh = tkinter.DoubleVar()
end_mosh = tkinter.DoubleVar()

rangebar = RangeSliderH(frame_right, [start_mosh, end_mosh], Width=510, Height=63,
                        bgColor=root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]),line_color="black",
                        bar_color_outer=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][0],
                        bar_color_inner=customtkinter.ThemeManager.theme["CTkCheckbox"]["checkmark_color"][1],min_val=0, max_val=1, show_value=False,
                        line_s_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][0])

label_seconds1 = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Start: 0s",width=1)
label_seconds2 = customtkinter.CTkLabel(master=frame_right,anchor='w',text="End: 0s",width=1)
label_segment = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Choose Segment:",width=1)

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
label_p = customtkinter.CTkLabel(master=frame_right,anchor='w',text="P-frames (Delta):",width=1)
label_segment = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Choose Segment:",width=1)

varp = tkinter.IntVar()
delta = customtkinter.CTkEntry(frame_right, placeholder_text="1",validate='key', validatecommand=(validation, '%P'),
                               width=100, textvariable=varp, placeholder_text_color="grey70", height=30, border_width=2,
                               corner_radius=10)
varp.set(1)

#Frame Rangebar for repeat and rise modes
start_frame_mosh = tkinter.DoubleVar()
end_frame_mosh = tkinter.DoubleVar()

rangebar2 = RangeSliderH(frame_right, [start_frame_mosh, end_frame_mosh], Width=510, Height=63,
                         bgColor=root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]),line_color="black",
                         bar_color_outer=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][0],
                         bar_color_inner=customtkinter.ThemeManager.theme["CTkCheckbox"]["checkmark_color"][1],min_val=0, max_val=1, show_value=False,
                         line_s_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"][0])

label_showframe1 = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Start Frame: 0",width=1)
label_showframe2 = customtkinter.CTkLabel(master=frame_right,anchor='w',text="End: 0",width=1)
label_segment2 = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Choose Frame Segment:",width=1)

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
    
label_mid = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Start Point: 0.5",width=1)
mid_point = customtkinter.CTkSlider(master=frame_right, width=500,progress_color="black", fg_color="black",
                                    from_=0, to=1, number_of_steps=10, command=lambda value: label_mid.configure(text="Start Point: "+str(round(value,1))))
mid_point.set(0.5)

#Some options for sort mode
keepsort = customtkinter.CTkCheckBox(master=frame_right, text="Keep First Frames", onvalue=0, offvalue=1)
reversesort = customtkinter.CTkCheckBox(master=frame_right, text="Reverse", onvalue=False, offvalue=True)

#Options for ffglitch modes
hw_auto = customtkinter.CTkSwitch(master=frame_right,text="HW Acceleration \n(Auto)",onvalue=1, offvalue=0)
labelk = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Keyframes:",width=1)
kf = customtkinter.CTkComboBox(master=frame_right,height=30, width=150, values=["1000", "100", "10", "1"])
kf._entry.config(validate='key', validatecommand=(validation, '%P'))

#Widget for Shuffle mode 
shuf_label = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Chunk Size: 1",width=1)
shuf_slider = customtkinter.CTkSlider(master=frame_right, width=500, from_=1, to=0, number_of_steps=1,
                                      command=lambda value:shuf_label.configure(text="Chunk Size: "+str(int(value))))
shuf_slider.set(1)

#Widget for Fluid mode
fluid_label = customtkinter.CTkLabel(master=frame_right,anchor='w',text="Amount: 5",width=1)
slider_fluid = customtkinter.CTkSlider(master=frame_right, width=500, from_=1, to=20, number_of_steps=100,
                                       command=lambda value:fluid_label.configure(text="Amount: "+str(int(value))))
slider_fluid.set(5)

#Stretch mode widget
v_h = customtkinter.CTkSwitch(frame_right,text="Horizontal Stretch", onvalue=1, offvalue=0)

#Button for motion transfer mode
def open_MT():
    global vfile
    vfile = tkinter.filedialog.askopenfilename(filetypes =[('Vector File', ['*.mp4','*.avi','*.mov','*.mkv']),('All Files', '*.*')])
    if vfile:
        mt_button.configure(fg_color='grey', text=os.path.basename(vfile))
    else:
        mt_button.configure(fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"], text="OPEN VIDEO")
        vfile = ''
    
mt_button = customtkinter.CTkButton(master=frame_right, text="OPEN VIDEO", width=520, height=30, compound="right",command=open_MT)

#Button for custom script mode
scriptfile = ''

def open_script():
    global scriptfile
    scriptfile = tkinter.filedialog.askopenfilename(filetypes =[('Script File', ['*.js','*.py']),('All Files', '*.*')])
    if scriptfile:
        scriptbutton.configure(fg_color='grey', text=os.path.basename(scriptfile))
    else:
        scriptbutton.configure(fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"], text='OPEN SCRIPT')
        scriptfile = ''
        
scriptbutton = customtkinter.CTkButton(master=frame_right, text="OPEN SCRIPT", width=520, height=30, compound="right",command=open_script)

#Dynamic UI functions for each widget
def rangeslider(x):
    if x==1:
        rangebar.place(x=20,y=210)
        label_seconds1.place(x=25,y=200)
        label_seconds2.place(x=470,y=200)
        label_segment.place(x=25,y=170)
    else:
        rangebar.place_forget()
        label_segment.place_forget()
        label_seconds1.place_forget()
        label_seconds2.place_forget()
def rangeslider2(x):
    if x==1:
        if (current=="Rise"):
            rangebar2.place(x=20,y=260)
            label_showframe1.place(x=25,y=250)
            label_showframe2.place(x=470,y=250)
            label_segment2.place(x=25,y=220)
        else:
            rangebar2.place(x=20,y=210)
            label_showframe1.place(x=25,y=200)
            label_showframe2.place(x=470,y=200)
            label_segment2.place(x=25,y=170)
    else:
        rangebar2.place_forget()
        label_showframe1.place_forget()
        label_showframe2.place_forget()
        label_segment2.place_forget()
def mid(x):
    if x==1:
        mid_point.place(x=20,y=210)
        label_mid.place(x=25,y=170)
    else:
        mid_point.place_forget()
        label_mid.place_forget()
def killoption(x):
    if x==1 or x==2 or x==3:
        label_kill.place(x=25,y=170)
        slider_kill.place(x=20,y=200)
    else:
        label_kill.place_forget()
        slider_kill.place_forget()
def positionslider(x):
    if x==1:
        label_frame1.place(x=25,y=230)
        position_frame.place(x=20,y=260)
    else:
        label_frame1.place_forget()
        position_frame.place_forget()
def framekeep(x):
    if x==1:
        keepframe.place(x=250,y=300)
    elif x==2:
        keepframe.place(x=250,y=240)
    else:
        keepframe.place_forget()
def audiokeep(x):
    if x==1:     
        keepaudio.place(x=400,y=300)
    elif x==2:
        keepaudio.place(x=400,y=240)
    else:
        keepaudio.place_forget()
def ctimes(x):
    if x==1:
        ctime.place(x=110,y=300)
        label_ctime.place(x=25,y=300)
        if current=="Water Bloom":
            varn.set(20)
        else:
            varn.set(1)
    else:
        ctime.place_forget()
        label_ctime.place_forget()
def pdelta(x):
    if x==1:
        delta.place(x=135,y=275)
        label_p.place(x=25,y=275)
        if current=="Repeat":
            varp.set(5)
    elif x==2:
        delta.place(x=135,y=170)
        label_p.place(x=25,y=170)
        if current=="Glide":
            varp.set(5)
    else:
        delta.place_forget()
        label_p.place_forget()
def sortoptions(x):
    if x==1:
        keepsort.place(x=30, y=170)
        reversesort.place(x=300, y=170)
    else:
        keepsort.place_forget()
        reversesort.place_forget()
def ffgassist(x):
    if x==1:
        hw_auto.place(x=25, y=170)
        labelk.place(x=300,y=170)
        kf.place(x=380,y=170)
    else:
        hw_auto.place_forget()
        labelk.place_forget()
        kf.place_forget()
def shuf(x):
    if x==1:
        shuf_label.place(x=25,y=220)
        shuf_slider.place(x=20,y=250)
    else:
        shuf_label.place_forget()
        shuf_slider.place_forget()
def fluidwidget(x):
    if x==1:
        fluid_label.place(x=25,y=220)
        slider_fluid.place(x=20,y=250)
    else:
        fluid_label.place_forget()
        slider_fluid.place_forget()
def h_v(x):
    if x==1:
        v_h.place(x=25,y=220)
    else:
        v_h.place_forget()
def mtwid(x):
    if x==1:
        mt_button.place(x=20,y=230)
    else:
        mt_button.place_forget()
def custom(x):
    if x==1:
        scriptbutton.place(x=20,y=230)
    else:
        scriptbutton.place_forget()

#Main function to update the widgets
def dynamic():
    global current, showwidgets
    allwidgets = [audiokeep, positionslider, killoption, framekeep,
                ctimes, pdelta, rangeslider, rangeslider2, mid, sortoptions, ffgassist, fluidwidget, h_v, custom, mtwid, shuf]
    for i in allwidgets:
        i(0)
        
    showwidgets = []
    if (current=="Bloom") or  (current=="Pulse") or (current=="Pulse") or(current=="Overlap"):
        showwidgets=[audiokeep, positionslider, killoption, framekeep, ctimes]
        u=1
    elif (current=="Jiggle"):
        showwidgets=[positionslider, audiokeep, killoption, framekeep]
        u=1
    elif (current=="Void") or (current=="Reverse") or (current=="Invert") or (current=="Random"):
        showwidgets=[killoption,audiokeep, framekeep]
        u=2
    elif (current=="Classic"):
        showwidgets=[rangeslider, pdelta]
        u=1
    elif (current=="Glide"):
        showwidgets=[pdelta]
        u=2
    elif (current=="Repeat") or (current=="Rise"):
        if (current=="Rise"): 
            showwidgets=[rangeslider2, ffgassist]
        else:
            showwidgets=[rangeslider2, pdelta]
        u=1
    elif (current=="Echo"):
        showwidgets=[mid]
        u=1
    elif (current=="Sort"):
        showwidgets=[sortoptions]
        u=1
    elif ((current=="Buffer") or (current=="Sink") or (current=="Mirror") or (current=="Shear") or (current=="Noise")
         or (current=="Delay") or (current=="Slam Zoom") or (current=="Invert-Reverse") or (current=="Shift") or (current=="Zoom")
         or (current=="Slice")or (current=="Vibrate") or (current=="Stop")):
        showwidgets=[ffgassist]
        u=1
    elif (current=="Fluid"):
        showwidgets=[ffgassist, fluidwidget]
        u=1
    elif (current=="Stretch"):
        showwidgets=[ffgassist, h_v]
        u=1
    elif (current=="Motion Transfer"):
        showwidgets=[ffgassist, mtwid]
        u=1
    elif (current=="Custom Script"):
        showwidgets=[ffgassist, custom]
        u=1
    elif (current=="Shuffle"):
        showwidgets=[ffgassist, shuf]
        u=1
    elif (current=="Water Bloom"):
        showwidgets=[ffgassist, positionslider, ctimes]
        u=1
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
            sfile = ofile[:-4]+"_datamoshed_"+current+'.'+optionmenu_1.get()
            nf = 0
            while os.path.exists(sfile):
                nf = nf+1
                sfile = ofile[:-4]+"_datamoshed_"+current+'('+str(nf)+')'+'.'+optionmenu_1.get()
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
        tkinter.messagebox.showinfo("No Video imported!","Please import a video file!")
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
            tomato.mosh(infile=ifile, outfile=mfile, m=current.lower(), c=varn.get(), n=int(position_frame.get()),
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
                classic.Datamosh(ifile, mfile,s=int(start_mosh.get()),e=int(end_mosh.get()),p=varp.get(), fps=vid.get_meta_data()['fps'])
            elif current=="Repeat":         
                repeat.Datamosh(ifile, mfile, s=int(start_frame_mosh.get()), e=int(end_frame_mosh.get()), p=varp.get(), fps=vid.get_meta_data()['fps'])
            elif current=="Glide":
                pymodes.library.glide(varp.get(), ifile, mfile)
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
                        tkinter.messagebox.showinfo("No Vector File imported!", "Please choose the video from where you want to extract the vector motion.")
                        button_mosh.configure(state=tkinter.NORMAL)
                        button_open.configure(state=tkinter.NORMAL)
                        ProcessLabel.configure(text='Choose any secondary video file for transfering the vectors!')
                        return
            elif current=="Shuffle":
                    basic_modes.library(ofile, mfile, mode=4, size=int(shuf_slider.get()), gop=kf.get())
            elif current=="Rise":
                    basic_modes.library(ofile, mfile, mode=5, s=int(start_frame_mosh.get()), e=int(end_frame_mosh.get()-start_frame_mosh.get()), gop=kf.get())
            elif current=="Water Bloom":
                    basic_modes.library(ofile, mfile, mode=6, f=int(position_frame.get()), r=varn.get(), gop=kf.get())
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
    except Exception as e:
        warnings.warn(str(e))
    
    #Check the result and complete the task
    if os.path.exists(sfile):
        tkinter.messagebox.showinfo("Exported!", "File exported successfully, \nFile Location:" +str(sfile))
        ProcessLabel.configure(text="Last used: "+last_used)
    else:
        tkinter.messagebox.showerror("Oops!", "Something went wrong! \nPlease recheck the settings and try again.")
        ProcessLabel.configure(text='Recheck the settings and try again!')
        
    button_open.configure(state=tkinter.NORMAL)
    button_mosh.configure(state=tkinter.NORMAL)
            
#Bottom Widgets
ProcessLabel = customtkinter.CTkLabel(master=frame_right, width=400, height=30,corner_radius=10, text="START DATAMOSHING!", fg_color=("white", "gray38"))
ProcessLabel.pack(padx=10, pady=10, fill="x", expand=True, side="left")

button_mosh = customtkinter.CTkButton(master=frame_right, height=30,width=110,corner_radius=10, text="MOSH", command=Threadthis)
button_mosh.pack(padx=(0,10), pady=10, fill="x", side="right")

root.mainloop()

#--------------------------------------------------------------------#
