import os
import subprocess

def convert_video_to_wav(input_file, output_file):
    with open('temp_video.mp4', 'wb') as f:
        f.write(input_file)

    ffmpeg_cmd = [
        "ffmpeg",
        "-i", "temp_video.mp4",
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-y",
        output_file
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True, shell=True)
        return True,"Successfully converted!"
    except subprocess.CalledProcessError as e:
        return True,"Conversion failed"