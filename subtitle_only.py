

from moviepy.editor import VideoFileClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.tools.subtitles import TextClip
from moviepy.editor import CompositeVideoClip

def  add_subtitles_with_srt(video_file, srt_path):
    # Load the video clip
    video_clip = video_file
    generator = lambda txt: TextClip(txt, font="Arial-Bold", fontsize=100,stroke_color="black", stroke_width=4, color="yellow", method='caption', size=video_clip.size)
    sub_clip = SubtitlesClip(srt_path, generator)
    result = CompositeVideoClip((video_clip, sub_clip), size=video_clip.size)
    return result

  
