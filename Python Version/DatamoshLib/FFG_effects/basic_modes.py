#Author: Akash Bora
import os, shutil, subprocess, random, json
from pathlib import Path
import numpy as np
DIRPATH = Path(os.path.dirname(os.path.realpath(__file__)))
ffgac = str(DIRPATH.parent.parent).replace(os.sep, '/')+"/FFglitch/ffgac"
ffedit = str(DIRPATH.parent.parent).replace(os.sep, '/')+"/FFglitch/ffedit"

def library(input_video, output, mode, extract_from="", fluidity=0, size=0, s=0, e=0, vh=0, gop=1000, r=0, f=0):
        def get_vectors(input_video):
            subprocess.call(f'"{ffgac}" -i "{input_video}" -an -mpv_flags +nopimb+forcemv -qscale:v 0 -g "{gop}"' +
                            ' -vcodec mpeg2video -f rawvideo -y tmp.mpg', shell=True)
            subprocess.call(f'"{ffedit}" -i tmp.mpg -f mv:0 -e tmp.json', shell=True)
            os.remove('tmp.mpg')
            f = open('tmp.json', 'r')
            raw_data = json.load(f)
            f.close()
            os.remove('tmp.json')
            frames = raw_data['streams'][0]['frames']
            vectors = []
            for frame in frames:
                try:
                    vectors.append(frame['mv']['forward'])
                except:
                    vectors.append([])
            return vectors
        def apply_vectors(vectors, input_video, output_video, method='add'):
            subprocess.call(f'"{ffgac}" -i "{input_video}" -an -mpv_flags +nopimb+forcemv -qscale:v 0 -g "{gop}"' +
                            ' -vcodec mpeg2video -f rawvideo -y tmp.mpg', shell=True)
            to_add = '+' if method == 'add' else ''
            script_path = 'apply_vectors.js'
            script_contents = '''
            var vectors = [];
            var n_frames = 0;
            function glitch_frame(frame) {
                let fwd_mvs = frame["mv"]["forward"];
                if (!fwd_mvs || !vectors[n_frames]) {
                    n_frames++;
                    return;
                }
                for ( let i = 0; i < fwd_mvs.length; i++ ) {
                    let row = fwd_mvs[i];
                    for ( let j = 0; j < row.length; j++ ) {
                        let mv = row[j];
                        try {
                            mv[0] ''' + to_add + '''= vectors[n_frames][i][j][0];
                            mv[1] ''' + to_add + '''= vectors[n_frames][i][j][1];
                        } catch {}
                    }
                }
                n_frames++;
            }
            '''
            with open(script_path, 'w') as f:
                f.write(script_contents.replace('var vectors = [];', f'var vectors = {json.dumps(vectors)};'))
            subprocess.call(f'"{ffedit}" -i tmp.mpg -f mv -s "{script_path}" -o "{output_video}"', shell=True)
            os.remove('apply_vectors.js')
            os.remove('tmp.mpg')
        def shuffle(output):
            if os.path.isdir("cache"):
                shutil.rmtree("cache")
            os.mkdir("cache")
            base=os.path.basename(input_video)
            fin="cache/"+base[:-4]+".mpg"
            subprocess.call(f'"{ffgac}" -i "{input_video}" -an -vcodec mpeg2video -f rawvideo -mpv_flags +nopimb -qscale:v 6 -r 30 -g "{gop}" -y "{fin}"')
            os.mkdir("cache/raws")
            framelist=[]
            subprocess.call(f'"{ffgac}" -i "{fin}" -vcodec copy cache/raws/frames_%04d.raw')
            frames=os.listdir("cache/raws")
            siz=size
            framelist.extend(frames)
            chunked_list=[]
            chunk_size=siz
            for i in range(0, len(framelist), chunk_size):
                    chunked_list.append(framelist[i:i+chunk_size])
            random.shuffle(chunked_list)
            framelist.clear()
            for k in frames[0:siz]:
                 framelist.append(k)
            for i in chunked_list:
                    for j in i:
                            if not j in framelist:
                                framelist.append(j)
            out_data = b''
            for fn in framelist:
               with open("cache/raws/"+fn, 'rb') as fp:
                   out_data += fp.read()
            with open(output, 'wb+') as fp:
                  fp.write(out_data)
                  fp.close()
            shutil.rmtree("cache")
        def rise(output):
            if os.path.isdir("cache"):
                shutil.rmtree("cache")
            os.mkdir("cache")
            base=os.path.basename(input_video)
            fin="cache/"+base[:-4]+".mpg"
            qua=''
            subprocess.call(f'"{ffgac}" -i "{input_video}" -an -vcodec mpeg2video -f rawvideo -mpv_flags +nopimb -qscale:v 6 -r 30 -g "{gop}" -y "{fin}"')
            os.mkdir("cache/raws")
            framelist=[]
            subprocess.call(f'"{ffgac}" -i "{fin}" -vcodec copy cache/raws/frames_%04d.raw')
            kil=e
            po=s
            if po==0:
                    po=1
            frames=os.listdir("cache/raws")  
            for i in frames[po:(po+kil)]:
                os.remove("cache/raws/"+i)
            frames.clear()
            frames=os.listdir("cache/raws")
            framelist.extend(frames)
            out_data = b''
            for fn in framelist:
               with open("cache/raws/"+fn, 'rb') as fp:
                   out_data += fp.read()
            with open(output, 'wb') as fp:
                  fp.write(out_data)
                  fp.close()
            shutil.rmtree("cache")
        def water_bloom(output):
            if os.path.isdir("cache"):
                shutil.rmtree("cache")
            os.mkdir("cache")
            base=os.path.basename(input_video)
            fin="cache/"+base[:-4]+".mpg"
            qua=''
            subprocess.call(f'"{ffgac}" -i "{input_video}" -an -vcodec mpeg2video -f rawvideo -mpv_flags +nopimb -qscale:v 6 -r 30 -g "{gop}" -y "{fin}"')
            os.mkdir("cache/raws")
            framelist=[]
            subprocess.call(f'"{ffgac}" -i "{fin}" -vcodec copy cache/raws/frames_%04d.raw')
            repeat=r
            po=f-1
            frames=os.listdir("cache/raws")
            for i in frames[:po]:
                    framelist.append(i)
            for i in range(repeat):
                    framelist.append(frames[po])
            for i in frames[po:]:
                    framelist.append(i)
            out_data = b''
            for fn in framelist:
               with open("cache/raws/"+fn, 'rb') as fp:
                   out_data += fp.read()
            with open(output, 'wb') as fp:
                  fp.write(out_data)
                  fp.close()
            shutil.rmtree("cache")
        def average(frames):
            if not frames:
                return []
            return np.mean(np.array([x for x in frames if x != []]), axis=0).tolist()
        def fluid(frames):
            average_length = fluidity
            if average_length==1:
                average_length=2
            return [average(frames[i + 1 - average_length: i + 1]) for i in range(len(frames))]
        def movement(frames):
            for frame in frames:
                if not frame:
                    continue
                for row in frame:
                    for col in row:
                        col[vh] = 0
            return frames
        if(mode==1):
            transfer_to=input_video
            vectors = []
            if extract_from:
                vectors = get_vectors(extract_from)
                if transfer_to == '':
                    with open(output, 'w') as f:
                        json.dump(vectors, f)
            apply_vectors(vectors, transfer_to, output)
        elif(mode==2):
            apply_vectors(movement(get_vectors(input_video)), input_video, output, method='')
        elif(mode==3):
            apply_vectors(fluid(get_vectors(input_video)), input_video, output, method='')
        elif(mode==4):
            shuffle(output)
        elif(mode==5):
            rise(output)
        elif(mode==6):
            water_bloom(output)
