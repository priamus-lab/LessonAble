import os
from pydub import AudioSegment

def wavsDuration(folderPath) -> int:
    total_duration = 0
    for file in os.listdir(folderPath):
        if file.endswith('.wav'):
            current_duration = len(AudioSegment.from_wav(folderPath + '/' + file))
            total_duration += current_duration
    total_duration = total_duration / 1000 # to seconds
    total_duration = total_duration / 60 # to minutes
    return total_duration
