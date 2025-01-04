## built-in libraries
import os
import sys

## third-party libraries
import moviepy.editor as mp
from pydub import AudioSegment

def trim_video_based_on_volume(video_path, output_path, silence_threshold=-50.0, chunk_size=100):
    video = mp.VideoFileClip(video_path)
    original_duration = video.duration
    
    if(video.audio is None):
        print(f"Warning: The video '{video_path}' does not have an audio track. Skipping trimming, likely a bad video.")
        video.write_videofile(output_path, codec='libx264')
        return 0  
    
    audio = video.audio
    audio_path = "temp_audio.wav"
    audio.write_audiofile(audio_path, codec='pcm_s16le') # type: ignore
    
    audio_segment = AudioSegment.from_file(audio_path)
    
    audio_duration = len(audio_segment)
    
    silence_duration = 0
    for i in range(0, audio_duration, chunk_size):
        chunk = audio_segment[i:i + chunk_size]
        if(chunk.dBFS < silence_threshold):
            silence_duration += chunk_size
        else:
            silence_duration = 0
        
        if(silence_duration >= chunk_size * 15):  # 1.5 seconds of silence
            break

    new_duration = (i - silence_duration) / 1000.0
    
    trimmed_video = video.subclip(0, new_duration)
    
    trimmed_video.write_videofile(output_path, codec='libx264')
    
    os.remove(audio_path)
    
    return original_duration - new_duration 

def process_directory(directory, append_str="-t", silence_threshold=-50.0, chunk_size=100):
    output_dir = os.path.join(directory, "trimmed_videos")
    if(not os.path.exists(output_dir)):
        os.makedirs(output_dir)
    
    significant_trims = []
    
    for filename in os.listdir(directory):
        if(filename.endswith(".mp4")):
            video_path = os.path.join(directory, filename)
            output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}{append_str}.mp4")
            duration_diff = trim_video_based_on_volume(video_path, output_path, silence_threshold, chunk_size)
            
            if(duration_diff > 5): 
                significant_trims.append((filename, duration_diff))

    if(len(significant_trims) > 0):
        print("\nVideos trimmed by more than 5 seconds (possible bad cuts):")
        print("-" * 60)
        for filename, duration in significant_trims:
            print(f"{filename}: trimmed {duration:.2f} seconds")
    else:
        print("\nNo videos were trimmed by more than 5 seconds.")

if(__name__ == "__main__"):
    if(len(sys.argv) < 2):
        print("Usage: python script.py <directory> [<append_str>]")
        sys.exit(1)
    
    directory = sys.argv[1]
    append_str = sys.argv[2] if len(sys.argv) > 2 else ""
    
    process_directory(directory, append_str)
