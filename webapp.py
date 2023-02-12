import streamlit as st
st.title("MASHUP")

name = st.text_input("Enter the Singer Name")
nov = st.text_input("Enter Number of videos")
nos = st.text_input("Enter Number of Seconds you want to trim the audio")
outputFile = st.text_input("Enter Output File name with .mp3 extension")
Email_id = st.text_input("Email ID", value="test@test.com")

submit = st.button("Submit")

if submit:
    from pytube import YouTube
    import sys
    import os
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
            # print(yt.title + " has been successfully downloaded.")    
        return namesList


    def merge(nov, namesList, nos, outputFile):
        nos = nos*1000
        for i in range(nov):
            sound1 = AudioSegment.from_file(str(namesList[i]))
            # print("-----CREATING MASHUP-----")
            # print("Extracting Sound from your audio file")
            extract = sound1[nos:]
            if(i==0):
                finalSound=extract
            else:
                finalSound = finalSound.append(extract,crossfade=1500)
        newFile = finalSound.export("{}".format(outputFile),format="mp3")
        # print("---MASHUP CREATED---")

        for i in range(nov):
            os.remove(namesList[i])
        return newFile

    def mail(audioFile, mailid):
        from email import message
        import os 
        from email.message import EmailMessage
        from re import sub
        import ssl
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        from email.mime.audio import MIMEAudio
        from pathlib import Path

        email_sender = 'rohit206thapar@gmail.com'
        password = 'viohznyupsttwxen'
        email_receiver = mailid

        # subject = "Mashup"
        # body = """ 
        #     Please find the below attachment 
        # """

        message = MIMEMultipart()
        message['from'] = email_sender
        message['to'] = email_receiver
        message['subject'] = "MASHUP by ROHIT THAPAR"
        message.attach(MIMEText(" Please find the below attachment "))
        # message.attach(MIMEAudio(Path(audioFile).read_bytes(), 'rb'))

        with smtplib.SMTP(host="smtp.gmail.com", port = 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(email_sender, password)
            smtp.send_message(message)
            st.write("Sent....")

    name = name
    nov = int(nov)
    nos = int(nos)
    mailID = Email_id
    outputFile = outputFile
    res=searchVids(name,nov)
    namesList=downloadVids(nov,res)
    audioFile = merge(nov, namesList, nos,outputFile)
    mail(audioFile, mailID)

    

   