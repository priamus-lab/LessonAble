from lesson_generation.video.generate_video import generate_video
from common.config_loader import load_config

c = load_config('/home/Ciro/Desktop/LessonAble/lesson_generation/config.json')
generate_video(c)