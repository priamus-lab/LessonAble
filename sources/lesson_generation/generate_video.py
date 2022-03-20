import argparse
from curses import meta
from importlib.metadata import metadata
from typing import final

import ffmpeg
import imageio
import numpy as np
from common.gdownload import gdownload
from common.video_common import (VideoExpression, expression, hasExpression,
                                 sentence_without_expression)
from skimage.transform import resize


### 1|Hello it'me, Ciro.|11(duration in seconds)
## here there will not be any expression because we will use nlp
def process_chuncks(chuncks_metadata_path, expression_based: bool):
    with open(chuncks_metadata_path, 'r') as f:
        lines = f.readlines()

    meta_data = []
    sub_meta_data = []
    for line in lines:
        chunk_number, sentence, duration = line.split('|')
        if hasExpression(sentence.rstrip()):
            #sentence ends with '.?!' or '.!?(2)'
            # var initialization
            final_chunk_number = 0
            final_sentence = ''
            final_duration = 0
            final_expression = VideoExpression(0)

            #checking if it's expression based
            if expression_based:
                final_expression = expression(sentence)

            # sub_metadata_empty?
            if sub_meta_data.count == 0:
                final_chunk_number = chunk_number
                final_sentence = sentence_without_expression(sentence)
                final_duration = duration.rstrip()
            else:
                sub_meta_data.append([chunk_number, sentence, duration])
                for (index, (chunck, sent, dur)) in enumerate(sub_meta_data):
                    if index == 0:
                        final_chunk_number = chunck
                    final_sentence = final_sentence + ' ' +  sent
                    final_duration += float(dur.rstrip())
                sub_meta_data = []
            meta_data.append([final_chunk_number, final_sentence, round(final_duration), final_expression])
        else:
            sub_meta_data.append([chunk_number, sentence, duration])
    return meta_data

## 0, hello everyone it's me,Ciro. 20.0  

#def sentiment_for_sentence(text):
   # meta_data = process_chuncks(chuncks_metadata_path)
    ## apply sentiment analysis
    #then generate the video.

## time 20 s : sentiment: good, bad or not known
def getGentleDrivingSequence(audio_duration, driving_sequence) -> ([], int):
    driving_duration = driving_sequence.get_meta_data()['duration']
    times_of_duplication = audio_duration / driving_duration

    fps = driving_sequence.get_meta_data()['fps']
    # want to have the same initial and end position
    if times_of_duplication < 2:
        splitting_frame_count = 2
    else:
        splitting_frame_count = round(times_of_duplication)

    frames_to_get = round((driving_duration / times_of_duplication)*fps)
    final_driving = []
    try:
        for im in driving_sequence:
            final_driving.append(im)
            frames_to_get -= 1
            if frames_to_get == 0:
                return (final_driving,splitting_frame_count)
    except RuntimeError:
        pass
    driving_sequence.close()



def generate_video_chunck(audio_duration, expression, sequence_folder_path, sequence_extension):
    # get the name based on the value of expression
    file_path =  sequence_folder_path + '/'+ str(expression.value) + sequence_extension
    driving_sequence = imageio.get_reader(file_path)
    # get the driving duration
    driving_duration = driving_sequence.get_meta_data()['duration']

    # gently driving sequence handling
    # given the driving duration and the audio duration, we want that the movement starts and ends in the same position:
    # that's how I have made it work
    # if audio duration > driving -> i.e a.d = 18s and d = 10s 
    # -> I calculate the timesOfDuplication by ceiling the result of ceil(a.d / d) -> i.e 2
    # then i get the 


    #calculating how many frame should we add or remove based on fps.
    fps = driving_sequence.get_meta_data()['fps']
    difference = abs(audio_duration-driving_duration)

    final_video = []
    difference_frame = round(difference*fps)
    total_frames = round(audio_duration * fps)
    final_driving, splitting_count = getGentleDrivingSequence(audio_duration, driving_sequence)

    for count in range(splitting_count):
        if count % 2 == 0:
            actual_driving = final_driving
        else:
            actual_driving = final_driving[::-1]
        try:
            for im in actual_driving:
                final_video.append(im)
                total_frames -= 1
                if total_frames == 0:
                    return final_video
        except RuntimeError:
            pass


    #             try:
    #                 for img in driving_sequence[::-1]:
    #                     if difference_frame == 0:
    #                         return final_video
    #                     final_video.append(img)
    #                     difference_frame -= 1
    #             except RuntimeError:
    #                 pass
    #             driving_sequence.close()
    # else:
    #     frames = audio_duration*fps
    #     try:
    #         for im in driving_sequence:
    #             if frames == 0:
    #                 return final_video
    #             final_video.append(im)
    #             frames -= 1
    #     except RuntimeError:
    #         pass
    #     driving_sequence.close()
    return final_video


        
# in future you could choose also the environment
def image_for_expression(expression, source_images_path):
    file_path =  source_images_path + '/'+ str(expression.value) + '.png'
    return imageio.imread(file_path)


def generate_video(c, driving_fps = 30, swap_face=True):
    chuncks_audio_path = c['audio']['chuncks_audio_path']
    expression_based = c['video']['expression_based']
    sequence_folder_path = c['video']['sequence_folder_path']
    sequence_ext = c['video']['sequence_ext']
    source_images_path = c['video']['source_images_path']
    foom_checkpoint_path = c['video']['foom_checkpoint_path']
    foom_config = c['video']['foom_config']
    output_path = c['video']['output_path']
    #final video
    driving_videos = []
    source_images = []
    #metadata from audio chuncks
    #metadata is calculated based on text if it's expression_based, with sentiment analysis if not.
    metadata = process_chuncks(chuncks_audio_path, expression_based)
    for (number, sentence, duration, expression) in metadata:
        driving_videos.append(generate_video_chunck(duration, expression, sequence_folder_path, sequence_ext))
        source_images.append(image_for_expression(expression, source_images_path))

    #source_image = resize(source_image, (256, 256))[..., :3]

    fps = driving_fps
    for idx,img in enumerate(source_images):
        source_images[idx] = resize(img, (256, 256))[..., :3]
    for idx, driving in enumerate(driving_videos):
        driving_videos[idx] = [resize(frame, (256, 256))[..., :3] for frame in driving]
 
    if swap_face:
        import sys
        sys.path.append('/home/Ciro/Desktop/LessonAble/lesson_generation/video/first-order-model')
        from demo import load_checkpoints, make_animation
        from skimage import img_as_ubyte
        from os.path import exists
        if not exists(foom_checkpoint_path):
            gdownload('1RO3-v031wXSfT5VC9_CLp-oAO59CUFfm', foom_checkpoint_path)
            print("FOOM.Vox model downloaded")
        generator, kp_detector = load_checkpoints(config_path=foom_config, 
                            checkpoint_path=foom_checkpoint_path)
   #
        array_of_predictions = []
        for idx,source_image in enumerate(source_images):
            prediction = make_animation(source_image, driving_videos[idx], generator, kp_detector, relative = True)
            array_of_predictions += prediction
#
    #save resulting video
        imageio.mimsave(output_path, [img_as_ubyte(frame) for frame in array_of_predictions], fps=fps)
    #else:
    #    imageio.mimsave('../generated.mp4', [img_as_ubyte(frame) for video in driving_videos for frame in video], fps=fps)
    # getting the face from the video
    #stream = ffmpeg.input(driving_video_path)
    #stream = ffmpeg.filter(stream, 'crop', 'crop=600:600:760:50')
    #-i /content/gdrive/My\ Drive/first-order-motion-model/07.mkv -ss 00:08:57.50 -t 00:00:08 -filter:v "crop=600:600:760:50" -async 1 hinton.mp4
     




#in the future i will make a config.json file

if __name__ == "__main__":
    """Run preprocessing process."""
    parser = argparse.ArgumentParser(
        description="Generate video.")
    parser.add_argument("--source_image_folder_path", type=str, required=True,
                        help="folder with source images of the author")
    parser.add_argument("--driving_video_folder", type=str, required=True,
                        help="folder with the driving videos")
    parser.add_argument("--out_path", default=None, type=str,
                        help="directory to save the output file.")
    parser.add_argument("--reference_text", default = None, type=str, required=True, help="the text related to this video.")
    parser.add_argument("--sequence_duration", default = None, type=int, help="set this parameter to change the sequence every amount of time equale to this parameter (set this in seconds). Remember to add more then a driving video in the videos folder")
    parser.add_argument("--automatic_textbased_driving_sequence", default = True, type=bool, help="if true, an NLP algorithm will choose the driving sequence based on the text.")
    parser.add_argument("--generated_audio_metadata_path", default = None, type=str, help="path to the metadata csv file related to the wavs generated.")
    parser.add_argument("--expression_based", default=True, type=bool)
    args = parser.parse_args()
    # load config
    image_folder_path = args.source_image_folder_path
    driving_video_folder_path = args.driving_video_folder
    text = args.reference_text
    sequence_duration = args.sequence_duration
    automatic_textbased_drivers = args.automatic_textbased_driving_sequence
    chuncks_metadata_path = args.generated_audio_metadata_path
    expression_based = args.expression_based
