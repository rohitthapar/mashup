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

    def mail(audioFile, mailID):

        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders

        fromaddr = "rohit206thapar@gmail.com"
        toaddr = mailID
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Your MASHUP"
        body = "Body_of_the_mail"
        msg.attach(MIMEText(body, 'plain'))
        filename = audioFile
        attachment = open("/audioFile", "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, "Password_of_the_sender")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()


    name = name
    nov = int(nov)
    nos = int(nos)
    mailID = Email_id
    outputFile = outputFile
    res=searchVids(name,nov)
    namesList=downloadVids(nov,res)
    audioFile = merge(nov, namesList, nos,outputFile)

    

    # def send_with_mailjet(sender, to, filename, base64encoded=""):
    #     from mailjet_rest import Client
    #     import os
    #     api_key = "3ab9d3a323b39d93b8592aa902d6db08"
    #     api_secret = '62e107b8f4bd191392609dd15be4915e'
    #     mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    #     data = {
    #         'Messages': [
    #             {
    #                 "From": {
    #                     "Email": sender,
    #                     "Name": "TOPSIS Calculator"
    #                 },
    #                 "To": [
    #                     {
    #                         "Email": to,
    #                         "Name": "Sir"
    #                     }
    #                 ],
    #                 "Subject": "Your TOPSIS Result",
    #                 "TextPart": "Topsis result analysis",
    #                 "HTMLPart": "<h3>Topsis result anaysis of the given input</h3>",
    #                 "Attachments": [
    #                     {
    #                         "ContentType": "text/csv",
    #                         "Filename": filename,
    #                         "Base64Content": encoded
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    #     result = mailjet.send.create(data=data)
    #     print(result.status_code)
    #     print(result.json())
    # import base64
    # data = open(filenameout, "r").read()
    # data = data.encode("utf-8")
    # encoded = base64.b64encode(data)
    # encoded = encoded.decode("utf-8")
    # send_with_mailjet("thaprt206@gmail.com", Email_id, "result.csv", encoded)
    # st.write("Email sent successfully , Please check your Spam folder also for mail")
    # os.remove(filenameout)