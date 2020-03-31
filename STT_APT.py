#!/usr/bin/env python
# coding: utf-8

# In[82]:


# -*- coding: utf-8 -*-

import os
import time
import requests
import json

import boto3

import speech_recognition as SR

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# In[87]:


audio_format = 'mp3'
Language='de-DE'
audio_name = 'x'+'.'+audio_format
audio_path = '/home/brian/Desktop/REWE/audio/'
job_name = "job_"+str(round(time.time()))
converted_audio_name = 'audio.wav'


###########____________AWS____________###################
job_uri = "s3://bucket1104test/"+"x."+audio_format
BucketName = 'bucket1104test'
#########################################################

###########____________google____________###################
############################################################

###########____________IBM____________###################
api_key         = '_ir8CSbBsCB3xfFmuwyqkb5dJXcHL1wbiyRMzcsPzRVQ'
speech2text_url = 'https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/8dd64a76-c56e-4b03-b4db-0a5c8bdb0693'

if_json_out = False
#########################################################


# In[93]:


def IBM_STT():
    print("converting audio..")
    os.system("echo 'y' | ffmpeg -i "+audio_path+audio_name+" "+audio_path+"/"+converted_audio_name+" 2>/dev/null")

    authenticator = IAMAuthenticator(api_key)
    service = SpeechToTextV1(authenticator=authenticator)
    service.set_service_url(speech2text_url)

    models = service.list_models().get_result()
    #print(json.dumps(models, indent=2))
    model = service.get_model(Language+'_BroadbandModel').get_result()
    #print(json.dumps(model, indent=2))

    with open(audio_path+converted_audio_name, 'rb') as audio_file:
        result_jsn = service.recognize(
                        audio=audio_file,
                        content_type='audio/wav',
                        timestamps=True,
                        model=Language+'_BroadbandModel',
                        word_confidence=True).get_result()

        if if_json_out:
            result_dic = json.dumps(result_jsn, indent=2)
            print(result_dic)

        out = result_jsn['results'][0]['alternatives'][0]['transcript']
        print(out)

    return out


# In[95]:


def Google_STT():
    sr = SR.Recognizer()

    print("converting audio..")
    os.system("echo 'y' | ffmpeg -i " + audio_path + audio_name + " " + audio_path + "/"+converted_audio_name+" 2>/dev/null")

    audio_file = SR.AudioFile(audio_path+converted_audio_name)

    with audio_file as source:
        audio = sr.record(source)

    return sr.recognize_google(audio_data=audio, language=Language)


# In[98]:


def AWS_Transcript():
    #------------------------------------------------------ Upload file to AWS s3
    s3 = boto3.client('s3')

    response = s3.list_buckets()
    #print(response)
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    #print(buckets)
    bucket_name = BucketName #buckets[0]

    s3.upload_file(audio_path+audio_name, Bucket=bucket_name, Key=audio_name)
    #------------------------------------------------------ Upload file to AWS s3


    transcribe = boto3.client('transcribe')

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=audio_format,
        LanguageCode=Language
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    #print(status)
    # took 160 sec

    out_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    #print(out_url)


    jsn = requests.get(out_url)
    open(audio_path+'out/'+'asrOutput.json', 'wb').write(jsn.content)

    with open(audio_path+'out/'+'asrOutput.json') as f:
        jsn_data = json.load(f)

    out = jsn_data['results']['transcripts'][0]['transcript']    
    print(out)   

    if False:
        start_time = status['TranscriptionJob']['StartTime']
        end_time = status['TranscriptionJob']['CompletionTime']
        print(start_time)
        print(end_time)
        
    return out    


# In[94]:


#IBM_STT()


# In[96]:


#Google_STT()


# In[99]:


#AWS_Transcript()


# In[ ]:





# In[5]:





# In[13]:





# In[ ]:





# In[27]:





# In[28]:





# In[ ]:





# In[33]:





# In[ ]:





# In[69]:





# In[59]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




