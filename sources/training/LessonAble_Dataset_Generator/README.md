# Lessonable Audio Dataset Generator
Run this code if you have a _.mp4_ or a _.mp3_ file associated with an _.srt_. 
The following lines of code will separate your audio in smaller wavs audios. The sentences pronunced in the wav audios will be written in the filelists.txt.

## Pre-requisites
A group of folders with an audio/video file and an srt file.

## Init
1. Clone this repo: git clone https://github.com/ciro97sa/LessonAble_Dataset_Generator
2. Install python requirements: pip install -r requirements.txt

``` bash
cd LessonAble_Dataset_Generator
mkdir raw_dataset
cd raw_dataset
mkdir lesson1
```

-add your video/audio file and the srt

## Dataset Generation 
1. Based on the code in the test.py you could create a LessonAble Audio Dataset.

The function to create the audio dataset is the following one:

``` python
def produceSpeechDataset(author, language, raw_dataset_path, output_path, minimum_words_for_sentence = 10, maximum_words_for_sentence = 2000, minimum_duration_in_seconds: float = 5, maximum_duration_in_seconds: float = 10)
```
- _author_: who is talking in the audio
- _language_: language used
- _raw_dataset_path_: the path to the directory created before(LessonAble_Dataset_Generator/raw_dataset/)
- _output_path_: the path to save the generated dataset

Example Usage:

``` python
from dataset_generator import produceSpeechDataset
objects = produceSpeechDataset('pippo', 'it', 'path_to_raw_data', 'output_dataset_it/', 1, 40, 1, 10)

```
There are additional functions to get some statistics on the dataset generated, such as get an histogram based on the durations or get the total durations of the audios.

``` python
from dataset_generator import create_histogram
from wavs_duration import wavsDuration

create_histogram(objects)
duration = wavsDuration('/Users/<user>/Desktop/LessonAble_Dataset_Generator/outdataset/author/wavs')
print(duration)
```
