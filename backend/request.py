from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from summarization import summarization
from send_email import send_mail
from video_to_audio import convert_video_to_wav
from audio_processing import process_audio
from audio_to_text import transcribe_audio
from text_processing import remove_stopwords
import os

app = FastAPI()

# Enable CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["POST"])

# File directories
UPLOAD_DIR = "uploaded_files"
OUTPUT_DIR = "converted_files"
PROCESSED_DIR = "processed_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Fetching file from local system
@app.post("/localsystem/")
async def localfile(file: UploadFile = File(...), recipients: str = Form(...)):
    # Split recipients by comma (assuming frontend sends it as a comma-separated string)
    recipients_list = recipients.split(',')

    # Save uploaded file
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # Define output file paths
    output_file = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file.filename)[0]}.wav")
    processed_output = os.path.join(PROCESSED_DIR, f"{os.path.splitext(file.filename)[0]}_processed.wav")

    # Convert video to audio
    success, message = convert_video_to_wav(file_location, output_file)

    if success:
        # Process audio and remove silence
        process_audio(output_file, processed_output)

        # Transcribe processed audio to text
        text = transcribe_audio(processed_output)

        # Preprocess text (e.g., remove stopwords)
        pre_text = remove_stopwords(text)

        # Summarize text and generate a plan of action
        summary, plan_of_action = summarization(pre_text)

        # Send the email
        send_mail(recipients_list, summary, plan_of_action)

        return {"message": "File processed and email sent successfully"}

    return {"message": message}

# Fetching file from OneDrive
@app.post("/one-drive/")
async def onedrive(file_name: str, file_content: bytes, recipients: str = Form(...)):
    # Split recipients by comma
    recipients_list = recipients.split(',')

    # Save file from OneDrive content
    file_location = os.path.join(UPLOAD_DIR, file_name)
    with open(file_location, "wb+") as file_object:
        file_object.write(file_content)

    # Define output file paths
    output_file = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file_name)[0]}.wav")
    processed_output = os.path.join(PROCESSED_DIR, f"{os.path.splitext(file_name)[0]}_processed.wav")

    # Convert video to audio
    success, message = convert_video_to_wav(file_location, output_file)

    if success:
        # Process audio and remove silence
        process_audio(output_file, processed_output)

        # Transcribe processed audio to text
        text = transcribe_audio(processed_output)

        # Preprocess text (e.g., remove stopwords)
        pre_text = remove_stopwords(text)

        # Summarize text and generate a plan of action
        summary, plan_of_action = summarization(pre_text)

        # Send the email
        send_mail(recipients_list, summary, plan_of_action)

        return {"message": "File processed and email sent successfully"}

    return {"message": message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
