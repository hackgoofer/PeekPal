import streamlit as st
from st_audiorec import st_audiorec
from pydub import AudioSegment
import io
import base64
import fal
from dotenv import load_dotenv

load_dotenv()


def whisper(data):
    handler = fal.apps.submit(
        "110602490-whisper",
        arguments={"url": data},
    )

    for event in handler.iter_events():
        if isinstance(event, fal.apps.InProgress):
            pass
            # print("Request in progress")
            # print(event)

    result = handler.get()
    return result.text


def mp3_data_to_data_url(mp3_data):
    # Convert the MP3 bytes to a base64 encoded string.
    mp3_base64 = base64.b64encode(mp3_data).decode("utf-8")

    # Create a data URL for the MP3 file
    mp3_data_url = f"data:audio/mp3;base64,{mp3_base64}"

    return mp3_data_url


# Function to convert base64 audio to MP3
def convert_to_mp3(audio_blob_base64):
    # Decode the base64 string to get the audio file
    audio_bytes = base64.b64decode(audio_blob_base64)
    audio_stream = io.BytesIO(audio_bytes)

    # Read the audio file using pydub (assuming it's in wav format)
    audio_segment = AudioSegment.from_file(audio_stream, format="wav")

    # Convert the audio to MP3
    mp3_stream = io.BytesIO()
    audio_segment.export(mp3_stream, format="mp3")

    return mp3_stream.getvalue()


def wav_to_data_url(wav_bytes):
    # Encode the WAV bytes as a base64 string
    wav_base64 = base64.b64encode(wav_bytes).decode("utf-8")
    # Create the data URL
    data_url = f"data:audio/wav;base64,{wav_base64}"
    return data_url


# Function to be called with the audio data, placeholder for your 'whisper' function
def process_audio(audio_blob):
    wav_data = wav_to_data_url(audio_blob)
    transcription = whisper(wav_data)
    return transcription


# Create the Streamlit app layout
st.markdown("<h1 style='text-align: center;'>PeekPal</h1>", unsafe_allow_html=True)

tra = ""
# Place the microphone in the center of the screen
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    wav_audio_data = st_audiorec()
    if wav_audio_data is not None:
        st.audio(wav_audio_data, format="audio/wav")
        tra = process_audio(wav_audio_data)

# Markdown field at the bottom
st.markdown("## Your transcriptions will appear here")
transcription_placeholder = st.empty()

# This would be where the transcription is updated
transcription_placeholder.markdown(f"### GOAL: {tra}")

# To run the app, save the code to a file (e.g., `app.py`) and
# use the command `streamlit run app.py`.
