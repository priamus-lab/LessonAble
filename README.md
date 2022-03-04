![Artboard](https://user-images.githubusercontent.com/34335234/156611971-2742923e-9196-4ce7-9f05-53f60511728f.png)
-------------

LessonAble is a pipelined methodology leveraging the concept of Deep Fakes for generating MOOC (Massive Online Open Course) visual contents directly from a lesson transcript.
To achieve this, the proposed pipeline consists of three main components: audio generation, video generation and lip-syncing.

This code is part of the paper: _Leveraging Deep Fakes in MOOC Content Creation_

| 📑  Original Paper                                            | 📑 Thesis                                                     | 🌀 Output Example                                             |
|--------------------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| [Paper](https://drive.google.com/file/d/1La0XjDs8wT8wZwLpFfd08Wo6cPtQmeLc/view?usp=sharing) | [Thesis](https://drive.google.com/file/d/1794_JqFbnubWddxWlu31Tp7uC7oWeU-W/view?usp=sharing) | [Example](https://drive.google.com/drive/folders/1fIjE4FXo0ul3RK6woEcjefQGUUrbQ5KO?usp=sharing) |

## Pipelined structure
![completed synthesis pipeline](https://user-images.githubusercontent.com/34335234/156781608-13eee86d-9067-4d98-8302-5f28a19d430d.png)

## Disclaimer
All results from this open-source code should only be used for research/academic/personal purposes only.
## Prerequisites
Prerequisites vary according to the chosen models for each component.
![Components](https://user-images.githubusercontent.com/34335234/156785352-fd93a319-0d7b-4ddb-b30d-ee1e038120c7.png)

- `Python 3.6` 
- NVIDIA GPU + CUDA cuDNN
- ffmpeg: `sudo apt-get install ffmpeg`
- Install necessary packages using `pip install -r requirements.txt`.
- Check the chosen models repository prerequisites.

## Getting the produced weights

| Component | Model       | Description                             | Link to the model |
|:---------:|:-----------:|:---------------------------------------:|:-----------------:|
| Audio     | ITAcotron 2 | Italian fine tuned model with this data |                   |
| Audio     | Tacotron 2  | English fine tuned model with this data |                   |
| Audio     | Tacotron 2  | English fine tuned model of Barack Obama with this data |                   |


## Data Collection
The data required to generate MOOC content is:
- At least 15 minutes of audio of the lecturer. Follow the [LessonAble Speech Dataset Generator](https://github.com/ciro97sa/LessonAble_Dataset_Generator) to generate an excellent dataset to train the Text to Speech model.
- A profile photo of the lecturer for every video expression.

### Generated dataset with the LessonAble Speech Dataset Generator
- [*Obama Voice*](https://drive.google.com/drive/folders/1z4MUnJ4G0ACxeQFEqt1zWfW6V5QM5Wjo?usp=sharing)
- [*Professor Carlo Sansone - ITALIAN*](https://drive.google.com/drive/folders/1iWgvF2M-zH6I213yWPYMkRRiuv7El14n?usp=sharing)
- [*Professor Carlo Sansone - ENGLISH*](https://drive.google.com/drive/folders/1HaF-0Q8UjDyNU0GHlC5Scmh_fmZKa1B8?usp=sharing)

## Audio Training
Once generated the lecturer's voice dataset, you're ready to training the Text to Speech model. Check the README of the Text to Speech models.

## Synthesis
After you're fine with the generated audio model, you just need to configure the lesson_generation_config.json file. Then, by calling:

``` python

from lesson_generation.video.generate_video import generate_video
from lesson_generation.audio.generate_audio import generate_audio
from lesson_generation.lipsyncing.Wav2Lip.lipsync import lipsync
from common.config_loader import load_config

config = load_config('/home/Ciro/Desktop/LessonAble/lesson_generation/config.json')

def generate(config):
    #1
    generate_audio(config)
    #2
    generate_video(config)
    #add both
    lipsync(config)
    
generate(config)
```


