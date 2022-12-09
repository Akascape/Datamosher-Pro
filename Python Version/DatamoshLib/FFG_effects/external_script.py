#Author: Akash Bora
import os, subprocess
from pathlib import Path
DIRPATH = Path(os.path.dirname(os.path.realpath(__file__)))
ffgac = str(DIRPATH.parent.parent).replace(os.sep, '/')+"/FFglitch/ffgac"
ffedit = str(DIRPATH.parent.parent).replace(os.sep, '/')+"/FFglitch/ffedit"

def mosh(input_video, output_video, mode, effect='', scriptfile='', gop=1000):
    if mode==1:
        script_path=scriptfile
    elif mode==2:
        script_path = str(DIRPATH).replace(os.sep, '/')+"/jscripts/"+effect+".js"
    subprocess.call(f'"{ffgac}" -i "{input_video}" -an -mpv_flags +nopimb+forcemv -qscale:v 0  -b:v 20M -minrate 20M -maxrate 20M -bufsize 2M -g "{gop}"' +
                        ' -vcodec mpeg2video -f rawvideo -y tmp.mpg', shell=True)
    subprocess.call(f'"{ffedit}" -i tmp.mpg -f mv -s "{script_path}" -o "{output_video}"', shell=True)
    os.remove('tmp.mpg')
