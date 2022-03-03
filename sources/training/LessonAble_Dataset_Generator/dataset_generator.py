import os
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from audio_sentence import Audio_Sentence
from sources.raw_data_preprocessing.string_processing import time_to_seconds, text_num_2_str, process_string
from sources.raw_data_preprocessing.srt_processing import split_text
from sources.raw_data_preprocessing.audio_processing import extract_audio
import mimetypes


def get_audiosentence_objects(author, language, srt_file_path, directory_name, starting_count: int, minimum_words_for_sentence: int, maximum_words_for_sentence: int, minimum_duration_in_seconds: float, maximum_duration_in_seconds: float):

    file = open(srt_file_path, "r")
    lines = file.readlines()
    file.close()

    non_empty_lines = [line for line in lines if line.rstrip().lstrip() != ""]
    audiosentence_tmp_array = []
    audiosentence_final_array = []

    count = starting_count
    for (index,line) in enumerate(non_empty_lines):

      if (line.strip().isdecimal() and index != len(non_empty_lines)-1):
        firstSentence = non_empty_lines[index+2].strip()
        secondSentence = ''
        if index + 3 < len(non_empty_lines) and non_empty_lines[index+3].strip().isdecimal() == False:
          secondSentence = non_empty_lines[index+3].strip()

        times = split_text(non_empty_lines[index+1].strip())
        start_time = str(time_to_seconds(times[0]))
        end_time = str(time_to_seconds(times[1]))

        audio_title = directory_name + '_' + str(index)
        sentence = firstSentence.strip() + " " + secondSentence.strip()
        tmp_obj = Audio_Sentence(author, sentence, start_time, end_time, audio_title)

        audiosentence_tmp_array.append(tmp_obj)

        if ((secondSentence.rstrip().endswith('.') or secondSentence.rstrip().endswith('?')) or (secondSentence == '' and (firstSentence.rstrip().endswith('.') or firstSentence.rstrip().endswith('?')))):
          final_sentence = ' '.join([x.sentence for x in audiosentence_tmp_array])
          final_sentence = process_string(final_sentence, language)
          final_audio_title = directory_name + '_' + str(count)
          
          # set if the minimum_words is respected
          final_obj = Audio_Sentence(author, final_sentence, audiosentence_tmp_array[0].start_time, audiosentence_tmp_array[len(audiosentence_tmp_array) - 1].end_time, final_audio_title)
          num_of_words = len(final_obj.sentence.split())
          duration = final_obj.duration()
          if (num_of_words >= minimum_words_for_sentence and num_of_words < maximum_words_for_sentence and duration <= maximum_duration_in_seconds and duration >= minimum_duration_in_seconds):
            count += 1
            audiosentence_final_array.append(final_obj)

          # reset
          audiosentence_tmp_array = []
    return audiosentence_final_array


def produceSpeechDataset(author, language, raw_dataset_path, output_path, minimum_words_for_sentence = 10, maximum_words_for_sentence = 2000, minimum_duration_in_seconds: float = 5, maximum_duration_in_seconds: float = 10):
  tmp_audio_url = 'tmp_audio.wav'
  os.mkdir(output_path)
  author_path = output_path+author
  wavs_path = author_path+'/wavs/'
  os.mkdir(author_path)
  os.mkdir(wavs_path)

   # an output folder called 'wavs' and a 'metadata.csv' file will be generated
  f = open(author_path + "/filelists" + ".txt", "w", encoding="utf-8")
  objects = []
  for root, subdirectories, files in os.walk(raw_dataset_path):
    for subdirectory in subdirectories:
      wavs_count = 0
      #initialize variables
      subtitle_objects = []
      print('\n Processing ' + subdirectory + ' directory...')
      for filename in os.listdir(raw_dataset_path + subdirectory):
        # get the mp4 and get its audio as .wav file. Saving this audio as 'audio.wav'
        mimetypes.init()
        mimestart = mimetypes.guess_type(filename)[0]

        if mimestart != None:
           mimestart = mimestart.split('/')[0]
        if mimestart in ['video']:
          extract_audio(root+subdirectory+ '/'+filename, tmp_audio_url)
        # get the .srt file and getting the SentenceObjects.
        if filename.lower().endswith('.srt'):
          subtitle_objects = get_audiosentence_objects(author, language, root+subdirectory+'/'+filename, subdirectory, wavs_count, minimum_words_for_sentence, maximum_words_for_sentence, minimum_duration_in_seconds, maximum_duration_in_seconds)
          wavs_count += (len(subtitle_objects)-1)
      # for each subtitle_object generated we cut the extracted audio in the interval (start_time-->end_time) 
      # and write the output audio in the wavs_path. Adding also the informations of the output audio in the .csv file
      for obj in subtitle_objects:
        audio_title = obj.audio_title
        ext = '.wav'
        sentence = obj.sentence.strip()
        if sentence.endswith('.') == False and sentence.endswith('?') == False:
          sentence += '.'
        f.write('wavs/' + audio_title + ext + '|' + sentence + '\n')
        obj.write_audiosentence(tmp_audio_url, wavs_path, True, True)
      objects += subtitle_objects
  if os.path.exists(tmp_audio_url):
      os.remove(tmp_audio_url)
  f.close()
  return objects


def create_histogram(objects): # input will be an array of Audio Sentence
  durations = list(object.duration() for object in objects)
  # formula to calculate the bins
  bins = 20
  #int((np.max(durations) - np.min(durations))/sqrt(len(durations)))
  plt.hist(durations, bins = bins)
  plt.show()

def get_total_duration(objects):
  durations = list(object.duration() for object in objects)
  return sum(durations)
