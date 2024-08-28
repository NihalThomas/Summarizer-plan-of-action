import streamlit as st
from file_from_onedrive import get_file_content, list_items_in_folder, get_access_token
from api import convert_video_to_wav
import os
from audio_to_text import transcribe_audio
import requests
from audio_processing import process_audio
from text_processing import remove_stopwords
from summarization import summarize_text

# Constraints for the generator

constraints = """Identify Type of meeting: Sales pitch, team meeting, project update, client meeting(Choose one among the given options).
Emotion or tone: Professional, enthusiastic, urgent, persuasive.
Specific industry or topic: Technology, healthcare, finance.
Any particular focus: Introducing a new product, discussing performance, setting goals, etc.
Summarize the text and generate 5 plan of action from meeting
Also make the Type of meeting, Emotion or tone:, Specific industry or topic:, Any particular focus:, Summary and plan of action in bold and increase the size
"""

# Predefined credentials

client_id = 'CLIENT_ID'
client_secret = 'CLIENT SECRET ID'
tenant_id = 'TENANT ID'
site_id = 'SITE_ID'
drive_id = 'DRIVE_ID'

# Streamlit app
def home_page():
    st.title("Meeting Summarizer & Plan of Action Generator using NLP")

    token = get_access_token(tenant_id, client_id, client_secret)
    items = list_items_in_folder(site_id, drive_id, token)
    if items:
        item_names = {item['name']: item['id'] for item in items}
        selected_item_name = st.selectbox("Select a file:", list(item_names.keys()))
        selected_item_id = item_names[selected_item_name]
        st.write(f"Selected file: {selected_item_name}")

        if st.button("Summarize"):
            file_content = get_file_content(site_id, drive_id, selected_item_id, token)
            if file_content:
                audio_output_path = 'output_audio.wav'
                convert_video_to_wav(file_content, audio_output_path)
                process_output = "Silence.wav"
                process_audio(audio_output_path, process_output)
                trans = transcribe_audio(process_output)
                processed = remove_stopwords(trans)
                summ = summarize_text(processed, constraints)

                st.session_state['summary'] = summ
                st.write(summ)