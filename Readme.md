# Datamosher Pro
<br><b>Datamoshing is a cool video effect and if you also want to create this glitch effect with your videos easily, you are in the right place!</b>
<br><p align='center'><img src="https://user-images.githubusercontent.com/89206401/141642297-7c62cf6f-7024-430f-88a2-c9cbbf0dc655.png"></p>
<br>➤Why I made this?
<br>I was also looking for some good datamoshing software and I found that for datamoshing, you have to either use those old softwares like Avidemux or have to look for some paid plugins, so I created my own GUI based application that is Datamosher Pro which is a free project. It contains 17 different effects which can replicate any type of datamoshing style. With Datamosher Pro, you can quickly and easily datamosh your videos (supports mp4, gif, avi, mkv etc).
# How to Install?
You can either use the python based version for viewing logs and changing source code if you want, but if you are looking for faster renders then download the windows executable version of Datamosher Pro from the release page: 
<br>[⬇️DOWNLOAD⬇️](https://github.com/Akascape/Datamosher-Pro/releases/tag/Datamosher_Prov1.4)
<br>There is no malware or difference in the exe version as the same python version is converted to .exe using Auto-Py-To-Exe Converter.
<br>Note: For python users, make sure you have all the assets saved in the same folder. Modules will be automatically downloaded if not installed, so no need to worry.
# How to Use?
•Input the video file first (supported formats- mp4, gif, avi + more will be added if you demand")
<br>•Choose the desired datamosh mode, then select the export format
<br>•Use advance options to get more accurate results
<br>•Uncheck the highest quality box if needed (export time will be reduced)
<br>•Click on the datamosh button, then wait for a few seconds
<br>•Then your video will be moshed, see the video in the directory
<br>NOTE: audio glitching is not available for all modes!
# Effects Info:
c=Glitch Size; n=Frame Frequency
<b>
<br>All effects:
<br>•Fluid - this is a ffglitch effect which gives a smooth liquid type transition to the video (NEW)
<br>•Repeat - this repeats a series of p frames which gives a melting effect (NEW)
<br>•Motion - a powerful ffglitch feature where you can transfer the vector motion data of one video to a different one (NEW)
<br>•Stretch - stretches the p-frames vertically (NEW)
<br>•Glide - duplicates number of n frames and show it as a flow before reaching the p-frame
<br>•Sort - sorts video frames by data size in a rapid movement
<br>•Echo - duplicates the single video and apply the mosh in the midpoint
<br>•Shake - shakes the pixel movement throughout the video
<br>•Classic - uses the traditional ffmpeg way to change the files and then remove the i-frames
<br>•Random - randomizes frame order
<br>•Reverse - reverse frame order
<br>•Invert - switches each consecutive frame witch each other
<br>•Bloom - duplicates c times p-frame number n
<br>•Pulse - duplicates groups of c p-frames every n frames
<br>•Overlap - copy group of c frames taken from every nth position
<br>•Jiggle - take frame from around current position. n parameter is spread size.
<br>•Void - gives a clean output but with distorted pixels</b>
<br>
<br>➤How to use Advanced Options?
<br>The advanced tab is very useful and you can use it to get accurate results.
<br>•Glitch Size - tells how often to glitch (for modes that support it)
<br>•Frame Frequency - tells how many frames to apply in the glitch (for modes that support it)
<br>•First Frame - tells whether to keep first video frames
<br>•Kill frames - tells max framesize to kill while cleaning
<br>You can try experimenting with the values and see the results.
# User Interface:
<br><img src="https://user-images.githubusercontent.com/89206401/142208408-6970448d-fe9d-4e60-aac6-21809aefcfca.png">
<br>➤More Info about this project:
<br>The effects are inspired from ItsKaspar's [tomato.py](https://github.com/itsKaspar/tomato), Joe Friedl's [pymosh](https://github.com/grampajoe/pymosh) and [FFglitch](https://ffglitch.org/). The main issue with datamoshing is conversion, most of the files need avi structure to mosh but in Datamosher Pro you can use any video file type including mp4, avi, gif, mov, mkv +more. The files are first converted to the correct file format using ffmpeg without losing much quality and then the effect is applied and then again the corrupted file is converted to stable version using the same process so that the output video can be directly used in other softwares for further editing without any error. A raw file option is also available if needed. You will not find this type of GUI program anywhere with so many free effects, I hope there is no error in the program but if you find any bug then raise an issue. You can also help to make new datamosh effects. All the logo and designs are created by me. <br>Thanks! Made by Akash Bora (a.k.a Akascape).
<br>
<br>DATAMOSH MADE EASY!
<br>Current Version=1.4
