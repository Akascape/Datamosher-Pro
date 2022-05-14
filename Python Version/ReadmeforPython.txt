#Read this to use the python version.
This version is comparitively lower in size and works the same inside python environment.
Things to setup before running the python file:
The GUI of Datamosher-Pro.py given in this source code version is optimised for Windows; for other OS, download the python version from release page.
1) First setup ffglitch if you are using this repo only. (See readme.txt inside ffglitch folder to download ffglitch)
(Make sure you make it Unix executable if you are on Mac and also give permission)
Note: No need to setup the ffglitch if you downloaded the python version from release page as all the versions are pre-provided there
2) After doing that, run the datamosher-pro.py file and click yes if module error pops up and let the modules get downloaded.
If it doesn't work then install the modules manually-
# Modules you need to install:
-- tkinter 
If not installed then use-
(pip install tk) or (sudo apt-get install python3-tk)
-- numpy
(pip install numpy)
-- imageio 
(pip install imageio)
-- imageio-ffmpeg 
(pip install imageio-ffmpeg)
# For Mac, you need to install one more module:
-- tkmacosx
(pip install tkmacosx)
3) Do not delete or move any assets or folder that are linked with the main file or else it will show error.
After the setup the application will open and you can try datamoshing.
