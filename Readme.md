# Datamosher Pro
<br>Datamoshing is an effect that really looks cool and if you also want to make this glitch effect with your videos, you are in the right place!
![icon](https://user-images.githubusercontent.com/89206401/138873267-16f152e7-b61a-4fc2-a215-1cb66a004f13.png)
<br>➤Why I made this?
<br>I was also looking for good datamoshing softwares, you can either have to use those old softwares like Avidemux or have to look for some paid plugins, but I created my own GUI based application that is Datamosher Pro which is a free project. It contains 7 different effects and more will be added in future, you can also help to make new effects. With Datamosher Pro, you can quickly and easily datamosh your videos(supports mp4, gif, avi, etc).
<br>
<br>➤How to Install?
<br>You can either use the python based version for viewing logs and changing source code if you want, but if you are looking for faster renders then download the executable version of Datamosher Pro from the release pagehttps:(https://github.com/Akascape/Datamosher-Pro/releases/tag/Datamosher_Prov1.1.exe)
<br>There is no malware or difference in the exe version(as the same python version is converted to .exe using Auto-Py-To-Exe Converter).
<br>Note: For python users, make sure you have all the assets with the python file and Imageio module installed in your system if not then open CMD and type"pip install imageio" and it will be installed.
<br>
<br>➤How to Use?
<br>•Input the video file first (supported formats- mp4, gif, avi + more will be added if you demand")
<br>•Choose the desired datamosh mode, then select the export format"
<br>•Use advance options to get more accurate results"
<br>•Then just click on the datamosh button, then wait for a few seconds"
<br>•Then your video will be moshed, see the video in the directory"
<br>•Note that if you mosh the same files in the same location again, then the new moshed file will replace the old file.
<br>
<br>➤Effects Info:
<br>(c is Glitch Frequency and n is Frame Frequency)
<br>random - randomizes frame order
<br>reverse - reverse frame order
<br>invert - switches each consecutive frame witch each other
<br>bloom - duplicates c times p-frame number n
<br>pulse - duplicates groups of c p-frames every n frames
<br>overlap - copy group of c frames taken from every nth position
<br>jiggle - take frame from around current position. n parameter is spread size.
<br>classic - uses classic ffmpeg way to corrupt videos (*new)
<br>
<br>➤How to use Advanced Options?
<br>The advanced tab is very useful and you can use it to get accurate results.
<br>Glitch Frequency - tells how often to glitch (for modes that support it)
<br>Frame Frequency - tells how many frames in the glitch (for modes that support it)
<br>Ignored First Frame - tells whether to keep first video frames
<br>Kill frames - tells max framesize to kill while cleaning
<br>You can try around changing the values from 50-100 and see the results, you can visit https://github.com/itsKaspar/tomato.git to view more examples about the advanced tab.
<br>
<br>➤User Interface:
<br>![Screenshot 2021-10-26 220159](https://user-images.githubusercontent.com/89206401/138922164-4c78f673-050e-4513-a3d2-6208e836cabc.png)
<br>
<br>➤More Info about this project:
<br>The effects are all inspired from ItsKaspar's https://github.com/itsKaspar/tomato.git but it can only handle .avi file structure, but in Datamosher Pro you can use any video file type including mp4, avi, gif. The files are first converted to avi file using Imageio without losing any quality and then the effect is applied and then again the corrupted file is converted to stable version using the same process so that the output video can be directly used by other softwares without any error. A raw form option is also available if needed. You will not find this type of GUI program anywhere, I hope there is no error in the software but if you saw any bug then raise an issue. All the logo and designs are created by me. <br>Thanks! Made by Akash Bora (a.k.a Akascape).
<br>
<br>DATAMOSH MADE EASY!
<br>Current Version=1.1

