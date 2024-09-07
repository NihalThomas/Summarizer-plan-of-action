import os
import subprocess

def convert_video_to_wav(input_file, output_file):

    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-y",
        output_file
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True, shell=True)
        os.remove(input_file)
        return True,"Successfully converted!"
    except subprocess.CalledProcessError as e:
        return True,"Conversion failed"