from common.gdownload import gdownload
import subprocess, platform

def lipsync(config):
    wav2lip_checkpoint = config['video']['wav2lip_checkpoint_path']
    wav_path = config['audio']['output_path']
    video_path = config['video']['output_path']
    output_path = config['lesson_output_path']
    tmp_wav2lipout_path = config['video']['wav2lip_temp_folder']
    from os.path import exists
    if not exists(wav2lip_checkpoint):
        gdownload('1a0BVIHxkBkj32ts9wnsCQN_c2GykmKCl', wav2lip_checkpoint)
        print("Wav2Lip model downloaded")
    p = subprocess.Popen(['python', '/home/Ciro/Desktop/LessonAble/lesson_generation/lipsyncing/Wav2Lip/inference.py', '--checkpoint_path', wav2lip_checkpoint, "--tmp_folder_path", tmp_wav2lipout_path, '--face', video_path, '--audio', wav_path, '--outfile', output_path])
    output, errors = p.communicate()

