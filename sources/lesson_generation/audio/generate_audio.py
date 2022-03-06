from email.mime import audio
import sys

from attr import has
sys.path.append('/home/Ciro/Desktop/LessonAble/')
from common.config_loader import load_config
from common.video_common import re,regex, hasExpression
from moviepy.editor import concatenate_audioclips, AudioFileClip
import os
sys.path.append('/home/Ciro/Desktop/LessonAble/training/Audio/ItalianMozillaTTS/TTS-master/')
from italian_synthesis import italian_synthesis
from english_synthesis import english_synthesis

def splitter(n, s):
    pieces = s.split()
    return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

def generate_audio(c):
    LANGUAGE = c['language']
    OUT_PATH = c['audio']['output_path']
    
    # processing the text
    LESSON_TEXT_PATH = c['lesson_text_path']
    CHUNCKS_PATH = c['audio']['chuncks_audio_path']
    with open(LESSON_TEXT_PATH) as f:
        text = f.read()
        # ends without any expression, we add it.
        if hasExpression(text) == False:
            text += '(0)'
        expressions = re.findall(regex(),text)
        sentences = re.split(regex(), text.rstrip())
        sentence_list = list(filter(None, sentences))

        audios_path = []
        chunks_files = []
        count = 0
        for index, sentence in enumerate(sentence_list):
            if len(sentence.split()) > 18:
                split = splitter(18, sentence)
                arr = list(split)
                length = len(arr)
                for idx, piece in enumerate(arr):
                    out_name = str(count) + '.wav'
                    if LANGUAGE == 'it':
                        italian_synthesis(c, out_name, piece)
                    else:
                        english_synthesis(c, out_name, piece)
                    audios_path.append(out_name)
                    count += 1
                    if idx == length-1:
                        chunks_files.append(str(count) + '|' + piece + expressions[index])
                    else:
                        chunks_files.append(str(count) + '|' + piece)   
            else:
                out_name = str(count) + '.wav'
                if LANGUAGE == 'it':
                    italian_synthesis(c, out_name, sentence)
                else:
                    print('english')
                count += 1
                audios_path.append(out_name)
                chunks_files.append(str(count) + '|' + sentence + expressions[index])
        
 
        for idx,audiofile in enumerate(audios_path):
            audios_path[idx] = '/home/Ciro/Desktop/LessonAble/' + audiofile
        
        concatenate_audio_moviepy(audios_path, chunks_files, CHUNCKS_PATH, OUT_PATH)

def concatenate_audio_moviepy(audio_clip_paths, chunks_files, CHUNCKS_PATH, output_path):
    """Concatenates several audio files into one audio file using MoviePy
    and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    file = open(CHUNCKS_PATH, 'w')
    for idx,chunk in enumerate(chunks_files):
        chunks_files[idx] += '|' + str(clips[idx].duration) + '\n'
        file.write(chunks_files[idx])
    
    file.close()

    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)

    