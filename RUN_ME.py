
from pexelsapi.pexels import Pexels
import requests
from moviepy.editor import VideoFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import CompositeVideoClip
from moviepy.video.fx.all import resize
import cv2
import os
from moviepy.editor import *
import random
import subtitle_only #subtitles my module
import random
import ai_module #my module
import YOUR_DATA #Contains all the api keys
import time 

SUCCESS_COUNT =0

def delete_temp_files(folder_path):
    for file in os.listdir(folder_path):
            try:           
                os.remove(os.path.join(folder_path, file))
            except:
                continue    


def resize_video(input_path, output_path, new_width, new_height):
    # Open the video file
    video_capture = cv2.VideoCapture(input_path)

    # Get the width and height of the video frame
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a VideoWriter object to write the resized video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    video_writer = cv2.VideoWriter(output_path, fourcc, 30, (new_width, new_height))

    # Read and resize each frame of the video
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (new_width, new_height))
        video_writer.write(resized_frame)

    # Release the video capture and writer objects
    video_capture.release()
    video_writer.release()



pexel = Pexels(YOUR_DATA.PEXELS_API_KEY)

MAX = random.randint(5,9)

#setting audio as audio file
audioclip = AudioFileClip(r"TEMP\speech.mp3")
audio_time = audioclip.duration

list_of_videos = []

try:
    popular_videos =  pexel.search_videos(query=f'{ai_module.TOPIC}', orientation='portrait', size='medium', color='', locale='en-US', page=1, per_page=MAX)
    

except:
    print("No search result") #default stock vids
    popular_videos =  pexel.search_videos(query='nature', orientation='portrait', size='', color='', locale='', page=1, per_page=MAX)    

index = 0

while index < MAX:
    try:
        print(popular_videos["videos"][index]['video_files'][0]['link'])
        video_url = popular_videos["videos"][index]['video_files'][0]['link']
        SUCCESS_COUNT+=1

    except:
        print(popular_videos["videos"][random.randint(0,SUCCESS_COUNT-1)]['video_files'][0]['link'])
        video_url = popular_videos["videos"][random.randint(0,SUCCESS_COUNT-1)]['video_files'][0]['link']
        continue

    # Make a GET request to the video URL
    response = requests.get(video_url)
    name = "video" + str(index)
    index +=1 
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Specify the file path where you want to save the video
        file_path = rf"TEMP\{name}.mp4"
        file_path_resized = rf"TEMP\{name}_resized.mp4"
        
        # Open the file in binary mode and write the video content-
        with open(file_path, "wb") as video_file:
            video_file.write(response.content)
            resize_video(file_path,file_path_resized,1080,1920)
            #os.system(rf"ffmpeg -i {file_path_resized} -vcodec libx264 {file_path}")
            clip = VideoFileClip(file_path_resized).subclip(0,audio_time/MAX)
            list_of_videos.append(clip)
            

          
                 
            
    else:
        print(f"Failed to download video. Status code: {response.status_code}")                
    

try:
    final = concatenate_videoclips(list_of_videos, method='compose') 
    # Save video clip
    final_out_sub= subtitle_only.add_subtitles_with_srt(final, r"TEMP\subtitles.srt")
    videoclip_out_final_w_audio = final_out_sub.set_audio(audioclip)
    time_now = time.time()
    videoclip_out_final_w_audio.write_videofile(rf"OUTPUT\OUTPUT_VIDEO_{str(time_now)}_file.mp4", fps=30, codec="libx264", audio_codec="aac")

    try:
        for video_clip in list_of_videos :
            video_clip.close()
    except:
        print("Video files not closed - can't clear TEMP files")

    delete_temp_files(rf"TEMP")

except:
    print("MAJOR ERROR VIDEO NOT RENDERED")    