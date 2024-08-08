from gtts import gTTS
import boto3
import os
import Twillio


def generateAudio(mytext):
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    name = "file1.mp3"
    myobj.save(name)
    os.system(name)
    print("Audio Generated")
    return name


def sendToS3Instance(file, bucket_name="YOUR_BUCKET"):
    s3 = boto3.client('s3', region_name='YOUR_REGION')
    s3.upload_file(file, bucket_name, file)
    audio_url_new = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file}, ExpiresIn=3600)
    print(audio_url_new)
    return audio_url_new


def completeProcess(text):
    _ = generateAudio(text)
    audio_url = sendToS3Instance(_)
    Twillio.call(audio_url, "PHONE_NUMBER_WITH_CODE")


