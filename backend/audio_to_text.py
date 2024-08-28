import whisper

def transcribe_audio(file):
    model = whisper.load_model("base")
    transcription = model.transcribe(file)
    return transcription["text"]

# Example usage:
# transcription = transcribe_audio("path/to/output.wav")
# print(transcription)
