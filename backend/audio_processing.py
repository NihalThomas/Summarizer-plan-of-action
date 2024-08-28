# audio_processing.py
from pydub import AudioSegment
from pydub.silence import split_on_silence

def process_audio(input_file, output_file):
    # Load your audio file
    audio = AudioSegment.from_file(input_file)

    # Split audio where silence is longer than 1 second and the silence is quieter than -40 dBFS
    chunks = split_on_silence(audio, min_silence_len=1000, silence_thresh=-40)

    # Combine chunks back into a single audio file without silence
    processed_audio = AudioSegment.empty()
    for chunk in chunks:
        processed_audio += chunk

    # Save the processed audio file
    processed_audio.export(output_file, format="wav")
