from lesson_generation.video.generate_video import generate_video
from lesson_generation.audio.generate_audio import generate_audio
from lesson_generation.lipsyncing.Wav2Lip.lipsync import lipsync
from common.config_loader import load_config

config = load_config('/home/Ciro/Desktop/LessonAble/lesson_generation/lesson_generation_config.json')

def generate(config):
    #1
    generate_audio(config)
    #2
    generate_video(config)
    #add both
    lipsync(config)
generate(config)


