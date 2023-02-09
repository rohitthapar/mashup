from pytube import YouTube
import os
import sys
from os import path 
from youtubesearchpython import VideosSearch

def mashup(name, nov):
    # name=input("Enter the name of the artist")
    # nov=int(input("Enter the no. of videos"))
    videosSearch = VideosSearch(str(name), limit = nov)
    res=[]
    for i in range(nov):
        res.append(videosSearch.result()['result'][i]['link'])
    print(res)
    namesList=[]
    for i in range(nov):
        yt = YouTube(str(res[i]))
        video = yt.streams.filter(only_audio=True).first()
    # print("Enter the destination address (leave blank to save in current directory)")
        destination =''
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        namesList.append(new_file)
        os.rename(out_file, new_file)
        print(yt.title + " has been successfully downloaded.")

def checkRequirements() :
    # print(len(sys.argv))
    if len(sys.argv) == 5:
        # singerName
        # print(sys.argv[2])
        singerName = sys.argv[1].lower()
        noOfVideos = int(sys.argv[2])
        #audioDuration
        audioDuration = int(sys.argv[3])
        # if audioDuration < 10:
        #     print("Audio duration to be cut should be more")
        # resultFileName
        resultFileName = sys.argv[-1].lower()
        if ".mp3" not in resultFileName:
            print("RESULT FILENAME SHOULD CONTAIN '.mp3'")
            return
        print(noOfVideos)
        mashup(singerName, noOfVideos)
            # return
        
        print("SAMPLE INPUT : python <programName> <singerName> <noOfVideos> <audioDuration> <resultFileName>")
        return

checkRequirements()
# mashup()