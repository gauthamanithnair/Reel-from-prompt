

import sys
import os
import random
import assemblyai as aai
import time
import YOUR_DATA

def make_folders():
    folder_path = "/OUTPUT"
    folder_path1 = "/TEMP"
    if not os.path.exists(folder_path):
        # Create the folder
        os.mkdir(folder_path)
        print(f"The folder '{folder_path}' has been created.")
    else:
        print(f"The folder '{folder_path}' already exists.")  

    if not os.path.exists(folder_path1):
        # Create the folder
        os.mkdir(folder_path1)
        print(f"The folder '{folder_path1}' has been created.")
    else:
        print(f"The folder '{folder_path1}' already exists.") 



make_folders()  #MAKES THE TEMPORARY FOLDERS


OPENAI_API_KEY = YOUR_DATA.OPENAI_API_KEY

TOPIC = input("ENTER A TOPIC - ONLY ONE WORD ALLOWED - ")

print(f"Topic is - {TOPIC}")

from openai import OpenAI
client = OpenAI()
from pathlib import Path

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You reel content writer. You specialize in making reel scripts that are ready for voice over. You dont demarkate the out-put. The output is as though you are speaking to someone "},
    {"role": "user", "content": f"Tell me a famous {TOPIC} quote and explain it beautifully not exceeding 120 words"},
    
  ],
   temperature=0.6,
  top_p=1
)

TEXT = response.choices[0].message.content
print(response.choices[0].message.content)

speech_file_path =rf"TEMP\speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="onyx",
  input=response.choices[0].message.content
)

response.stream_to_file(speech_file_path)

aai.settings.api_key = YOUR_DATA.ASSEMBLY_AI_API_KEY

transcript = aai.Transcriber().transcribe(speech_file_path)

try:
  subtitles = transcript.export_subtitles_srt(chars_per_caption= 15).upper()

except:
  subtitles = transcript.export_subtitles_srt(chars_per_caption= 20).upper()


try:
  os.remove(rf"TEMP\subtitles.srt")

except :
  pass

try:
  f  = open(rf"TEMP\subtitles.srt" , "a")
  f.write (subtitles)
  f.close()

except:
  print("SUBTITLE ERROR - NOW EXITING")
  time.sleep(5)
  sys.exit()
