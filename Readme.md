# Datamosher Pro
<br><b>Datamoshing is a cool video effect and if you also want to create this glitch effect with your videos easily, you are in the right place!</b>
<br><p align='center'><img src="https://user-images.githubusercontent.com/89206401/141642297-7c62cf6f-7024-430f-88a2-c9cbbf0dc655.png"></p>
<br>➤Why I made this?
<br>I was also looking for some good datamoshing software and I found that you have to either use those old softwares like Avidemux or have to look for some paid plugins to datamosh your videos, so I created my own GUI based application that is Datamosher Pro which is a free project. It contains `30+` different effects which can replicate any type of datamoshing style. With Datamosher Pro, you can quickly and easily datamosh your videos.
# How to Install?
You can either use the python based version for viewing logs and changing source code if you want, but if you are in windows and looking for faster renders then download the windows executable version of Datamosher Pro from the release page: 
<br>[`⬇️DOWNLOAD⬇️`](https://github.com/Akascape/Datamosher-Pro/releases/tag/Datamosher_Prov1.5)
<br>Don't worry, there is no malware or difference in the exe version as the same python version is converted to .exe using Auto-Py-To-Exe Converter.
<br>Note: For python users modules will be automatically downloaded if not installed, so no need to worry.
# How to Use?
• Input the video file first (supported formats- mp4, gif, avi, mov, mkv, wmv)
<br>• Choose the desired datamosh mode, then select the export format
<br>• Use advance options to get more accurate results
<br>• Uncheck the highest quality box if needed (export time will be reduced)
<br>• Click on the datamosh button, then wait for a few seconds
<br>• Then your video will be moshed, see the video in its directory
# Effects Info:
All Effects Info
<b>
<br>• `Buffer` - creates ring buffers to mosh (NEW)
<br>• `Delay` - another delaying ffglitch effect (NEW)
<br>• `Invert` Reverse - applies both inverse and reverse mode (NEW)
<br>• `Mirror` - does the mosh with ffglitch but with mirrored X (NEW)
<br>• `Noise` - makes large noisy mosh (NEW)
<br>• `Shear` - moves down the right side of te video and merge with the mosh (NEW)
<br>• `Shift` - shifts the block of the video upwards randomly (NEW)
<br>• `Sink` - drowns the next frame of the video with the previous one (NEW)
<br>• `Slam Zoom` - applies zoom with the sink effect (NEW)
<br>• `Slice` - Zooms and slices the video in parts randomy (NEW)
<br>• `Stop` - similar to sink but only stops the XY values randomly (NEW)
<br>• `Vibrate` - works as a randomizer (NEW)
<br>• `Zoom` - simply zoom inside the moshed video (NEW)
<br>• `Fluid` - this is a ffglitch effect which gives a smooth liquid type transition to the video
<br>• `Repeat` - repeats a series of p frames which gives the melting effect
<br>• `Motion` - a powerful ffglitch feature that can transfer the vector motion data from one video to a different one
<br>• `Stretch` - stretches the p-frames vertically
<br>• `Glide` - duplicates number of n frames and show it as a flow before reaching the p-frame
<br>• `Sort` - sorts video frames by data size in a rapid movement
<br>• `Echo` - duplicates the single video and apply the mosh effect in the midpoint
<br>• `Shake` - shakes the pixel movement throughout the video
<br>• `Classic` - uses the traditional ffmpeg way to change the files and then remove the i-frames
<br>• `Random` - randomizes frame order
<br>• `Reverse` - reverse frame order
<br>• `Invert` - switches each consecutive frame witch each other
<br>• `Bloom` - duplicates c times p-frame number n (c=Glitch Size; n=Frame Frequency)
<br>• `Pulse` - duplicates groups of c p-frames every n frames
<br>• `Overlap` - copy group of c frames taken from every nth position
<br>• `Jiggle` - take frame from around current position. n parameter is spread size.
<br>• `Void` - gives a clean output but with distorted pixels
</b>
<br>NOTE: audio glitching is not available for all modes!
<br>Major Effects you see for basic datamoshing: Classic, Bloom, Glide, Repeat, Motion, Fluid
<br>
<br>➤How to use Advanced Options?
<br>The advanced tab is very useful and you can use it to get accurate results.
<br>• `Glitch Size` - tells how often to glitch
<br>• `Frame Frequency` - tells how many frames to apply in the glitch
<br>• `First Frame` - tells whether to keep first video frames
<br>• `Kill Frames` - tells max framesize to kill while cleaning
<br>NOTE: Some modes may not support all the 4 advanced options.
<br>You can try experimenting with the values and see the results!
# User Interface:
<br><img src="https://user-images.githubusercontent.com/89206401/142208408-6970448d-fe9d-4e60-aac6-21809aefcfca.png">
## How It Works
The main issue with datamoshing is conversion of corrupted files but with Datamosher Pro you can use any video file type and get an usable datamoshed video file rendered. The files are first converted to the required file format using ffmpeg without losing much quality, then the effect is applied and the corrupted file is converted to stable version again using the same process so that the output video can be used directly in other softwares for further editing. All the unneccesary temp file will get deleted automatically.
## Conclusion
You will not find this type of GUI program anywhere with so many free effects only for datamoshing.
I hope there is no error in the program but if you find any bug then raise an issue. You can also help to make new datamosh effects.
<br>The effects are inspired from ItsKaspar's [tomato.py](https://github.com/itsKaspar/tomato), Joe Friedl's [pymosh](https://github.com/grampajoe/pymosh) and [FFglitch](https://ffglitch.org/). 
All the logo and designs are created by me. <br>Thanks! Made by Akash Bora (a.k.a `Akascape`).
<br>
<br>DATAMOSHING MADE EASY!
<br>Current Version=1.5
