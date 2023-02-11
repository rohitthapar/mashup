from youtubesearchpython import VideosSearch
from pytube import YouTube
from pydub import AudioSegment
import os
import sys

def searchVids(name, nov):
    # name=input("Enter the name of the artist")
    # nov=int(input("Enter the no. of videos"))
    videosSearch = VideosSearch(str(name), limit = nov)
    res=[]
    for i in range(nov):
        res.append(videosSearch.result()['result'][i]['link'])
    return res

def downloadVids(nov, res):
    namesList=[]
    for i in range(nov):
        yt = YouTube(str(res[i]))
        video = yt.streams.filter(only_audio=True).first()
        destination =''
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        namesList.append(new_file)
        # print()
        os.rename(out_file, new_file)
        print(yt.title + " has been successfully downloaded.")
    for i in range(nov):
        print(namesList[i])    

def merge(nov, namesList, EndSec,outputFile):
    # EndSec = int(input("Enter the End second "))
    EndSec=EndSec*1000
    for i in range(nov):
        sound1 = AudioSegment.from_file(namesList[i], format = "mp3")
        print("Extracting Sound from your audio file")
        # print(sound1)
        extract = sound1[10:EndSec]
        if(i==0):
            finalSound=extract
        else:
            finalSound = finalSound.append(extract,crossfade=1500)
    finalSound.export("${outputFile}.mp3",format="mp3")

def mashup():
    if len(sys.argv) != 5:
        print("How to use: python topsis.py inputfile.csv '1,1,1,1,1' '+,+,+,+,+' result.csv ")
        exit(1)
    else:
        # downloadFlag=0
        name = str(sys.argv[1])
        nov=int(sys.argv[2])
        EndSec=int(sys.argv[3])
        outputFile=str(sys.argv[4])
        res=searchVids(name,nov)
        # while not downloadFlag:
        namesList=downloadVids(nov,res)
        merge(nov, namesList, EndSec,outputFile)
    
if __name__ == "__main__":
    mashup()