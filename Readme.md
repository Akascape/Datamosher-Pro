# Datamosher Pro
<br><b>Datamoshing is a cool video effect and if you also want to easily create this glitch effect with your videos, you are in the right place!</b>
<br><p align='center'><img src="https://user-images.githubusercontent.com/89206401/141642297-7c62cf6f-7024-430f-88a2-c9cbbf0dc655.png"></p>
### Why I made this?
I was also looking for some good datamoshing software and I found that you have to either use those old softwares like Avidemux or have to look for some paid plugins to datamosh your videos, so I created my own GUI based application that is Datamosher Pro which is a free project. It contains `30+` different effects which can replicate any type of datamoshing style. With Datamosher Pro, you can quickly and easily datamosh your videos!
# DOWNLOAD
<br>[`⬇️Windows⬇️`](https://github.com/Akascape/Datamosher-Pro/releases/download/Datamosher_Prov1.5/Datamosher_Pro_win64.zip)             [`⬇️Python (Source Code)⬇️`](https://github.com/Akascape/Datamosher-Pro/releases/download/Datamosher_Prov1.5/Datamosher_Pro-python_version.zip)
# How to Install?
- For Windows version, just extract the downloaded zip file and run the Datamosher-Pro.exe to open it. (No installation setup required)
- For Python users, just run the Datamosher.py file. If any module error pops up then just click on yes and the required module will be downloaded automatically. Then the program is ready to use.
<br>Note: For python users who are not in windows, please download the correct version of ffglitch from ffglitch.org and extract it in inside the ffglitch folder of Datamosher pro. (Only windows version is given in this repo)
# How to Use?
• Input the video file first (supported formats- mp4, gif, avi, mov, mkv, wmv)
<br>• Choose the desired datamosh mode, then select the export format
<br>• Use advance options to get more accurate results
<br>• Uncheck the highest quality box if needed (export time will be reduced)
<br>• Click on the datamosh button, then wait for a few seconds
<br>• Then your video will be moshed and will be saved in the same directory
# Effects Info
### All Effects:
TIP: Major Effects used for basic datamoshing: Classic, Bloom, Glide, Repeat, Motion, Fluid
<b><br>• `Buffer` - creates ring buffers to mosh (NEW)
<br>• `Delay` - another delaying ffglitch effect (NEW)
<br>• `Invert-Reverse` - applies both inverse and reverse mode (NEW)
<br>• `Mirror` - does the mosh with ffglitch but with mirrored X (NEW)
<br>• `Noise` - makes large noisy mosh (NEW)
<br>• `Shear` - tilt the video clockwise and merges the mosh (NEW)
<br>• `Shift` - shifts random blocks of the video upwards (NEW)
<br>• `Sink` - drowns the next frame of the video with the previous one (NEW)
<br>• `Slam Zoom` - applies zoom with the sink effect (NEW)
<br>• `Slice` - Zooms and slices the video in parts randomy (NEW)
<br>• `Stop` - similar to sink but only stops the XY values randomly (NEW)
<br>• `Vibrate` - works as a randomizer (NEW)
<br>• `Zoom` - simply zooms inside the moshed video (NEW)
<br>• `Fluid` - this is a ffglitch's average effect which gives a smooth liquid type motion to the video
<br>• `Repeat` - repeats a series of p frames which gives the melting effect
<br>• `Motion` - a powerful ffglitch feature that can transfer the vector motion data from one video to a different one
<br>• `Stretch` - stretches the p-frames vertically
<br>• `Glide` - duplicates number of n frames and show it as a flow before reaching the p-frame
<br>• `Sort` - sorts video frames by data size in a rapid movement
<br>• `Echo` - duplicates the single video and apply the mosh effect in the midpoint
<br>• `Shake` - shakes the pixel movement throughout the video
<br>• `Classic` - uses the traditional ffmpeg way to corrupt the video and then remove the i-frames
<br>• `Random` - randomizes frame order
<br>• `Reverse` - reverse frame order
<br>• `Invert` - switches each consecutive frame witch each other
<br>• `Bloom` - duplicates c times p-frame number n (c=Glitch Size; n=Frame Frequency)
<br>• `Pulse` - duplicates groups of c p-frames every n frames
<br>• `Overlap` - copy group of c frames taken from every nth position
<br>• `Jiggle` - take frame from around current position. n parameter is spread size.
<br>• `Void` - gives a clean output but distorted by killing frames</b>
### How to use Advanced Options?
The advanced tab is very useful and you can use it to get accurate results.
<br>• `Glitch Size` - tells how often to glitch
<br>• `Frame Frequency` - tells how many frames to apply in the glitch
<br>• `First Frame` - tells whether to keep first video frames
<br>• `Kill Frames` - tells max framesize to kill while cleaning
<br>
<br>NOTE:
<br>- Some modes may not support all the 4 advanced options.
<br>- You can try experimenting with the values and see the results but don't put huge values.
<br>- Audio glitching is not available for all modes.
# UI
<br><img src="https://user-images.githubusercontent.com/89206401/142208408-6970448d-fe9d-4e60-aac6-21809aefcfca.png">
## How It Works?
The main issue with datamoshing is conversion of corrupted files but with Datamosher Pro you can use any video file and get an usable datamoshed video file. The files are first converted to the required file format using ffmpeg without losing much quality, then the effect is applied and the corrupted file is converted back to stable version using the same process so that the output video can be used directly in other editing softwares. All the unneccesary temp files get deleted automatically.
## Conclusion
You will not find this type of GUI program anywhere with so many free effects only for datamoshing.
I hope there is no error in the program but if you find any bug then raise an issue. You can also help to make new datamosh effects.
<br>The effects are inspired from ItsKaspar's [tomato.py](https://github.com/itsKaspar/tomato), Joe Friedl's [pymosh](https://github.com/grampajoe/pymosh) and [FFglitch](https://ffglitch.org/). 
All the logo and designs are created by me. <br>Thanks! Made by Akash Bora (a.k.a `Akascape`).
<br>
<br> DATAMOSHING MADE EASY!
### Current Version=1.5
