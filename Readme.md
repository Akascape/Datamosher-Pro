# Datamosher Pro
<br>Datamoshing is a cool video effect and if you also want to create this glitch effect with your videos, you are in the right place!
                          
 ![icon](https://user-images.githubusercontent.com/89206401/141642246-64e32eab-5583-4a52-8d81-6397979db56d.png)
<br>➤Why I made this?
<br>I was also looking for some good datamoshing software and I found that you have to either use those old softwares like Avidemux or have to look for some paid plugins, so I created my own GUI based application that is Datamosher Pro which is a free project. It contains 13 different effects which can replicate any type of datamoshing style. With Datamosher Pro, you can quickly and easily datamosh your videos (supports mp4, gif, avi, mov etc).
<br>
# How to Install?
<br>You can either use the python based version for viewing logs and changing source code if you want, but if you are looking for faster renders then download the windows executable version of Datamosher Pro from the release page: 
<br>[⬇️DOWNLOAD⬇️](https://github.com/Akascape/Datamosher-Pro/releases/tag/Datamosher_Prov1.2.exe)
<br>There is no malware or difference in the exe version as the same python version is converted to .exe using Auto-Py-To-Exe Converter.
<br>Note: For python users, make sure you have all the assets saved in the same folder. Modules will be automatically downloaded if not installed, so no need to worry.
<br>
# How to Use?
<br>•Input the video file first (supported formats- mp4, gif, avi + more will be added if you demand")
<br>•Choose the desired datamosh mode, then select the export format"
<br>•Use advance options to get more accurate results"
<br>•Click on the datamosh button, then wait for a few seconds"
<br>•Then your video will be moshed, see the video in the directory"
<br>NOTE: audio glitching is not available for all modes!
<br>
# Effects Info:
<br>c=Glitch Size; n=Frame Frequency
<br>All effects:
<br>•Glide - duplicates number of n frames and show it as a flow before reaching the p-frame (NEW)
<br>•Sort - sorts video frames by data size in a rapid movement (NEW)
<br>•Echo - duplicates the single video and apply the mosh in the midpoint (NEW)
<br>•Shake - shakes the pixel movement throughout the video (NEW)
<br>•Classic - uses the traditional ffmpeg way to change the files and then corrupt the videos by moving the pixels
<br>•Random - randomizes frame order
<br>•Reverse - reverse frame order
<br>•Invert - switches each consecutive frame witch each other
<br>•Bloom - duplicates c times p-frame number n
<br>•Pulse - duplicates groups of c p-frames every n frames
<br>•Overlap - copy group of c frames taken from every nth position
<br>•Jiggle - take frame from around current position. n parameter is spread size.
<br>•Void - gives a clean output but with distorted pixels
<br>
<br>➤How to use Advanced Options?
<br>The advanced tab is very useful and you can use it to get accurate results.
<br>•Glitch Size - tells how often to glitch (for modes that support it)
<br>•Frame Frequency - tells how many frames to apply in the glitch (for modes that support it)
<br>•First Frame - tells whether to keep first video frames
<br>•Kill frames - tells max framesize to kill while cleaning
<br>You can try around changing the values from 50-100 and see the results, you can visit [Tomato git](https://github.com/itsKaspar/tomato.git) to view more examples about the advanced tab.
<br>
# User Interface:
<br>![Screenshot 2021-10-26 220159](https://user-images.githubusercontent.com/89206401/138922164-4c78f673-050e-4513-a3d2-6208e836cabc.png)
<br>
<br>➤More Info about this project:
<br>The effects are inspired from ItsKaspar's [tomato.py](https://github.com/itsKaspar/tomato.git) and Joe Friedl's [pymosh](https://github.com/grampajoe/pymosh) which can only handle .avi file structures, but in Datamosher Pro you can use any video file type including mp4, avi, gif, mov, mkv +more. The files are first converted to avi file using Imageio-ffmpeg without losing much quality and then the effect is applied and then again the corrupted file is converted to stable version using the same process so that the output video can be directly used in other softwares for editing without any error. A raw file option is also available if needed. You will not find this type of GUI program anywhere with so many free effects, I hope there is no error in the program but if you find any bug then raise an issue. You can also help to make new datamosh effects. All the logo and designs are created by me. <br>Thanks! Made by Akash Bora (a.k.a Akascape).
<br>
<br>DATAMOSH MADE EASY!
<br>Current Version=1.3

