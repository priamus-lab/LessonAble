import wave
import noisereduce as nr
from pydub.audio_segment import AudioSegment
from scipy.io import wavfile
import os
import sys

def reduce_noise(wavPath):
    # load data
    rate, data = wavfile.read(wavPath)
    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    return reduced_noise, rate

def reduce_wavs_noise(wavsFolderPath, destinationFolder):
    for file in os.listdir(wavsFolderPath):
        if file.endswith('.wav'):
            reduced_noise, rate = reduce_noise(wavsFolderPath + '/' + file)
            wavfile.write(destinationFolder + '/' + file, rate, reduced_noise)
            
def main(args):
    if len(args) != 2: 
        print('Error')
    reduce_wavs_noise(args[0], args[1])
    

main(['/Users/cirosannino/Desktop/LJSpeech_dataset_generator/output_dataset_offical_en/sansone/wavs', '/Users/cirosannino/Desktop/LJSpeech_dataset_generator/removed_noise_wavs'])