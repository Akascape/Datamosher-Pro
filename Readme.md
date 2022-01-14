# Datamosher Pro
<br><b>Datamoshing is a cool video effect and if you also want to create this glitch in your videos, you are in the right place!
<br>With Datamosher Pro you can quickly and easily datamosh your videos!</b><br>
<br><p align='center'><img src="https://user-images.githubusercontent.com/89206401/141642297-7c62cf6f-7024-430f-88a2-c9cbbf0dc655.png"></p>
### Why I made this?
I was also looking for some good datamoshing software and I found that you have to either use those old softwares like Avidemux or have to look for some paid plugins, so I created my own python based application 'Datamosher Pro' which is a free project. It contains `30+` different effects which can replicate any type of datamoshing style.
# DOWNLOAD
### <p align='center'> [`⬇️Datamosher-Pro for Windows⬇️`](https://github.com/Akascape/Datamosher-Pro/releases/download/Datamosher_Prov1.6/Datamosher_Pro_win64.zip)     [`⬇️Python(Source Code)⬇️`](https://github.com/Akascape/Datamosher-Pro/releases/download/Datamosher_Prov1.6/Datamosher_Pro-python_version.zip) </p>
# How to Install?
- For Windows version, just extract the downloaded zip file and run the Datamosher-Pro.exe to open it. (No installation setup required)
- For Python users, just run the Datamosher-Pro.py file. If any module error pops up then just click on yes and the required module will be downloaded automatically. After installation of modules the program is ready to use.
<br>Note: For python users who are not in windows, please download the correct version of ffglitch from [ffglitch.org](https://ffglitch.org/) and extract it inside the ffglitch folder (only windows ffglitch is given in this repo).
# How to Use?
• Input the video file first (supported formats- mp4, gif, avi, mov, mkv, wmv)
<br>• Choose the desired datamosh mode and the export format
<br>• Use the advance options to get more accurate results
<br>• Check/uncheck the highest quality box for quality adjustments
<br>• Then simply click on the datamosh button and wait for a few seconds
<br>• After conversions, your video will be moshed and saved in the same directory
# Effects Info
### Effects List:
TIP: Major effects used for basic datamoshing: Classic, Bloom, Glide, Repeat, Motion Transfer, Rise, Fluid
| Effect Name     | Description                                                           |
| ----------------| --------------------------------------------------------------------- |
| Rise (NEW)      | another classic i and p frames removal effect|
| Shuffle (NEW)   | randomly shuffles chunks of video frames with the classic ffglitch datamosh|
| Buffer          | creates ring buffers to mosh|
| Delay           | another delaying ffglitch effect|
| Invert-Reverse  | applies both inverse and reverse mode|
| Mirror          | does the mosh with ffglitch but with mirrored X|
| Noise           | makes large noisy mosh|
| Shear           | tilt the video clockwise and merges the mosh|
| Shift           | shifts random blocks of the video upwards|
| Sink            | drowns the next frame of the video in the previous one|
| Slam Zoom       | applies zoom with the sink effect|
| Slice           | randomly zooms and slices the video in parts|
| Stop            | similar to sink but stops the XY values|
| Vibrate         | works as a randomizer|
| Zoom            | simply zooms inside the moshed video|
| Fluid           | this is a ffglitch's average effect which gives a smooth liquid type motion in the video|
| Repeat          | repeats a series of p frames which gives the melting effect|
| Motion Transfer | a powerful ffglitch feature that can transfer the vector motion data from one video to another. Make sure both videos have the same resolution, this effect is also known as style transfer/swap motion.|
| Stretch         | stretches the p-frames horizontally and vertically|
| Glide           | duplicates number of n frames and show it as a flow before reaching the p-frame|
| Sort            | sorts video frames by data size in a rapid movement|
| Echo            | duplicates the single video and apply the mosh effect in the midpoint|
| Shake           | randomly shakes the pixels/blocks throughout the video|
| Classic         | uses the traditional ffmpeg way to convert and corrupt the video by removing the i-frames|
| Random          | randomizes frame order|
| Reverse         | reverses frame order|
| Invert          | switches each consecutive frame witch each other|
| Bloom           | duplicates c times p-frame number n (c=Glitch Size; n=Frame Frequency)|
| Pulse           | duplicates groups of c p-frames every n frames|
| Overlap         | copy group of c frames taken from every nth position|
| Jiggle          | take frame from around current position. n parameter is spread size|
| Void            | gives a clean output but with distortion|
### How to use Advanced Options?
The advanced tab is very useful to get accurate results. The options are:
<br>• `Glitch Size` - tells how long/often to glitch
<br>• `Frame Frequency` - tells how many frames to apply in the glitch
<br>• `First Frame` - tells whether to keep the first video frames
<br>• `Kill Frames` - tells max framesize to kill while cleaning
<br>
<br>NOTE:
<br>- Some modes may not support all the 4 advanced options.
<br>- You can try experimenting with the values and see the results but don't put huge values.
<br>- Audio glitching is only available in few modes like classic and repeat.
# UI
<br><img src="https://user-images.githubusercontent.com/89206401/142208408-6970448d-fe9d-4e60-aac6-21809aefcfca.png">
## Demo
Demos will be uploaded soon!
## How It Works?
The main issue with datamoshing is conversion of corrupted files but with Datamosher Pro you can use any video file and get an usable datamoshed file. The video is first converted to the required file format using ffmpeg, then the effect is applied and the corrupted file is converted back to stable version using the same process so that the output video can directly be used in other editing softwares. All the unneccesary temp files get deleted automatically.
## Conclusion
You will not find this type of free software anywhere with so many free effects only for datamoshing. This program can be your companion while editing cool videos :)
<br>I hope there is no error in the program but if you find any bug then raise an issue. You can also help to make new datamosh effects.
<br>The effects are all inspired from ItsKaspar's [tomato.py](https://github.com/itsKaspar/tomato), Joe Friedl's [pymosh](https://github.com/grampajoe/pymosh) and [FFglitch](https://ffglitch.org/). 
All the logos and designs are created by me. <br>-Akash Bora
<br>Follow me : [`Akascape`](https://github.com/Akascape)
<br> Don't forget to give a ⭐!
<br>
<br> DATAMOSHING MADE EASY!
### Current Version-1.6.1
