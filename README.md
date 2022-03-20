# LessonAble

LessonAble is a pipelined methodology leveraging the concept of Deep Fakes for generating MOOC (Massive Online Open Course) visual contents directly from a lesson transcript.
To achieve this, the proposed pipeline consists of three main components: audio generation, video generation and lip-syncing.

This code is part of the paper: _Leveraging Deep Fakes in MOOC Content Creation_

| 📑  Original Paper                                            | 📑 Thesis                                                     | 🌀 Output Example                                             |
|:--------------------------------------------------------------:|:--------------------------------------------------------------:|:--------------------------------------------------------------:|
| [Paper](https://drive.google.com/file/d/1La0XjDs8wT8wZwLpFfd08Wo6cPtQmeLc/view?usp=sharing) | [Thesis](https://drive.google.com/file/d/1794_JqFbnubWddxWlu31Tp7uC7oWeU-W/view?usp=sharing) | [Example](https://drive.google.com/drive/folders/1fIjE4FXo0ul3RK6woEcjefQGUUrbQ5KO?usp=sharing) |

## Pipelined structure
![completed synthesis pipeline](https://user-images.githubusercontent.com/34335234/158707075-b18eb634-8a6c-4d71-b77b-378a4d5576a6.png)


## Disclaimer
All results from this open-source code should only be used for research/academic/personal purposes only.
## Prerequisites
Prerequisites vary according to the chosen models for each component.
![Components](https://user-images.githubusercontent.com/34335234/158707157-203a4db5-e63c-4c3c-bb75-46a1a9d5a153.png)


- `Python 3.6` 
- NVIDIA GPU + CUDA cuDNN
- ffmpeg: `sudo apt-get install ffmpeg`
- Install necessary packages using `pip install -r requirements.txt`.
- Check the chosen models repository prerequisites.

## Getting the produced weights

| Component | Model       | Description                             | Link to the model |
|:---------:|:-----------:|:---------------------------------------:|:-----------------:|
| Audio     | ITAcotron 2 | Italian fine tuned model with this [*dataset*](https://drive.google.com/drive/folders/1iWgvF2M-zH6I213yWPYMkRRiuv7El14n?usp=sharing) |[Model](https://drive.google.com/file/d/13ShpvlA06q9qHjRI-5Qp21XgygnlWZPx/view?usp=sharing)                   |
| Audio     | Tacotron 2  | English fine tuned model with this [*dataset*](https://drive.google.com/drive/folders/1HaF-0Q8UjDyNU0GHlC5Scmh_fmZKa1B8?usp=sharing) |[Model](https://drive.google.com/file/d/18tfOLdsHk20IqIwpY6eUJ8fRgIF_otf5/view?usp=sharing)                   |
| Audio     | Tacotron 2  | English fine tuned model of Barack Obama with this [*dataset*](https://drive.google.com/drive/folders/1z4MUnJ4G0ACxeQFEqt1zWfW6V5QM5Wjo?usp=sharing) |[Model](https://drive.google.com/file/d/1Gh2BqrkbVTJ1rK-NpGcpttbfsjBIjLxT/view?usp=sharing)                    |


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
After you're fine with the generated audio model, you just need to configure the [lesson_generation_config.json](https://github.com/priamus-lab/LessonAble/blob/main/sources/lesson_generation/lesson_generation_config.json) file. Then, by calling:

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

## Cite work
If you are willing to use our code, please cite our work through the following BibTeX entry:
```
@inproceedings{sannino2022lessonable,
title={LessonAble: Leveraging Deep Fakes in MOOC Content Creation},
author={Sannino, Ciro and Gravina, Michela and Marrone, Stefano and Fiameni, Giuseppe and Sansone, Carlo},
booktitle={International Conference on Image Analysis and Processing},
year={2022},
organization={Springer}
}
```
