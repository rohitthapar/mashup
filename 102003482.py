from pytube import YouTube
import os
import sys
# sys.path.append('/Users/rohitthapar/ffmpeg ')
from os import path 
from youtubesearchpython import VideosSearch
from pydub import AudioSegment 

def searchVids(name, nov):
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
    # for i in range(nov):
    #     print(namesList[i])    
    return namesList


def merge(nov, namesList, nos, outputFile):
    nos = nos*1000
    for i in range(nov):
        sound1 = AudioSegment.from_file(str(namesList[i]))
        print("-----CREATING MASHUP-----")
        print("Extracting Sound from your audio file")
        extract = sound1[nos:]
        if(i==0):
            finalSound=extract
        else:
            finalSound = finalSound.append(extract,crossfade=1500)
    finalSound.export("{}".format(outputFile),format="mp3")
    print("---MASHUP CREATED---")

    for i in range(nov):
        os.remove(namesList[i])

def mashup():
    if len(sys.argv) != 5:
        print("SAMPLE INPUT : python <programName> <singerName> <noOfVideos> <audioDuration> <resultFileName>")
        exit(1)
    else:
        name = str(sys.argv[1])
        nov=int(sys.argv[2])
        nos=int(sys.argv[3])
        outputFile=str(sys.argv[4])
        res=searchVids(name,nov)
        namesList=downloadVids(nov,res)
        merge(nov, namesList, nos,outputFile)
    
if __name__ == "__main__":
    mashup()