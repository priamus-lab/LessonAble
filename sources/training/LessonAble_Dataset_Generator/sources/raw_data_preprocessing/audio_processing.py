import moviepy.editor as mp
import subprocess

def extract_audio(videoName, unique_source_audio_path):
    subprocess.run( #converts the webm to wav using ffmpeg
        (['ffmpeg', '-y', '-i', videoName, unique_source_audio_path]))