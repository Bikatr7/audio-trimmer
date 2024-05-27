## built-in libraries
import os
import sys

## third-party libraries
import moviepy.editor as mp
from pydub import AudioSegment

def trim_video_based_on_volume(video_path, output_path, silence_threshold=-50.0, chunk_size=100):
    video = mp.VideoFileClip(video_path)
    
    ## Extract audio from the video
    audio = video.audio
    audio_path = "temp_audio.wav"
    audio.write_audiofile(audio_path, codec='pcm_s16le') # type: ignore
    
    audio_segment = AudioSegment.from_file(audio_path)
    
    ## Calculate the duration of the audio in milliseconds
    audio_duration = len(audio_segment)
    
    ## Analyze audio in chunks
    silence_duration = 0
    for i in range(0, audio_duration, chunk_size):
        chunk = audio_segment[i:i + chunk_size]
        if(chunk.dBFS < silence_threshold):
            silence_duration += chunk_size
        else:
            silence_duration = 0
        
        ## If silence duration exceeds a threshold, break the loop
        if(silence_duration >= chunk_size * 15):  # 1.5 seconds of silence
            break

    ## Calculate the new duration to trim the video
    new_duration = (i - silence_duration) / 1000.0
    
    trimmed_video = video.subclip(0, new_duration)
    
    ## Save the trimmed video
    trimmed_video.write_videofile(output_path, codec='libx264')
    
    ## Clean up temporary audio file
    os.remove(audio_path)

def process_directory(directory, append_str="-t", silence_threshold=-50.0, chunk_size=100):
    output_dir = os.path.join(directory, "trimmed_videos")
    if(not os.path.exists(output_dir)):
        os.makedirs(output_dir)
    
    for filename in os.listdir(directory):
        if(filename.endswith(".mp4")):
            video_path = os.path.join(directory, filename)
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}{append_str}.mp4")
            trim_video_based_on_volume(video_path, output_path, silence_threshold, chunk_size)

if(__name__ == "__main__"):
    if(len(sys.argv) < 2):
        print("Usage: python script.py <directory> [<append_str>]")
        sys.exit(1)
    
    directory = sys.argv[1]
    append_str = sys.argv[2] if len(sys.argv) > 2 else ""
    
    process_directory(directory, append_str)
