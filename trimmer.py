## third-party libraries
import moviepy.editor as mp
from pydub import AudioSegment

def trim_video_based_on_volume(video_path, output_path, silence_threshold=-50.0, chunk_size=100):

    video = mp.VideoFileClip(video_path)
    
    ## Extract audio from the video
    audio = video.audio
    audio_path = "temp_audio.wav"
    audio.write_audiofile(audio_path, codec='pcm_s16le')
    
    ## Load audio using pydub
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
        
        # If silence duration exceeds a threshold, break the loop
        if(silence_duration >= chunk_size * 15):  # 1.5 seconds of silence
            break

    ## Calculate the new duration to trim the video
    new_duration = (i - silence_duration) / 1000.0
    
    trimmed_video = video.subclip(0, new_duration)
    
    ## Save the trimmed video
    trimmed_video.write_videofile(output_path, codec='libx264')
    
    ## Clean up temporary audio file
    import os
    os.remove(audio_path)