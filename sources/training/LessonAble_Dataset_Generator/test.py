from dataset_generator import produceSpeechDataset
from dataset_generator import create_histogram
from sources.stats.wavs_duration import wavsDuration

objects = produceSpeechDataset('sansone', 'it', '/Users/cirosannino/Downloads/OneDrive_1_1-4-2022/', 'output_dataset_it_addhoc_new/', 1, 40, 1, 10)
#create_histogram(objects)
print(wavsDuration('/Users/cirosannino/Downloads/owavs'))