from pydub import AudioSegment
import shutil, os
from tkinter import filedialog

def choose_dir():
    cont = 0
    AudioSegment.ffmpeg = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    path = filedialog.askopenfilenames()
    for aux in path:
        file = os.path.basename(aux)
        print(aux)
        var = aux
        aux = file.split(".")
        if aux[1] == "mp3":
            print("mp3")
            with open(var, 'rb') as forigen:
                with open("D:/test/" + aux[0] + ".mp3", 'wb') as fdestino:
                    shutil.copyfileobj(forigen, fdestino)
                    cont += 1
        else:
            audio = AudioSegment.from_file(var, format=aux[1])
            audio.export("D:/test/" + aux[0] + ".mp3", format="mp3")
            cont += 1

        print(str(cont) + "de 433" )

choose_dir()