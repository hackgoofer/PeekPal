import streamlit as st
from st_audiorec import st_audiorec
from pydub import AudioSegment
import io
import base64
import fal
from dotenv import load_dotenv
from openai import OpenAI
import datetime
import time

client = OpenAI()
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
    return result['text']


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
    with st.form("audio_form"):
        wav_audio_data = st_audiorec()
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if wav_audio_data is not None:
            st.audio(wav_audio_data, format="audio/wav")
            tra = process_audio(wav_audio_data)

from main import get_screenshot

messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are a GPT4 Vision assitant bot - you will be given screenshots of the user's current screen, along with their intended goal. If they have not yet achieved their goal, you should offer suggestions for what they should do. Respond in short sentences and if any bullet points and emphasis, format them in markdown.",
            },
        ],
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                # "text": "According to the screenshot, what is the next step so that I can listen to the same song at the same time with a friend?",
                "text": "describe the screenshot",
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{get_screenshot()}"},
            },
        ],
    }
]
replies = []

# Display the screenshot in a Streamlit image component
screenshot = messages[1]['content'][1]['image_url']['url']
st.image(screenshot, caption='Current Screenshot')

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=messages,
    max_tokens=300,
)

reply = response.choices[0].message.content
print(reply)
replies.append((reply, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


# Markdown field at the bottom
st.markdown("## Your transcriptions will appear here")
transcription_placeholder = st.empty()

if tra:
    # Markdown field at the bottom
    st.markdown("## Goal")
    transcription_placeholder = st.empty()

    # This would be where the transcription is updated
    # transcription_placeholder.markdown(f"### GOAL: {tra}")
    transcription_placeholder.markdown(f"### GOAL")

    # Create a text area box that defaults to the `tra` variable
    user_input = st.text_area("Update your goal:", value=tra)
    # Update the `tra` variable with the user's input
    if user_input != tra:
        tra = user_input
        transcription_placeholder.markdown(f"### GOAL: {tra}")

if tra:
    messages.extend(
        [
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": reply},
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"According to the screenshot, what is the next step so to achieve the goal: {tra}",
                    },
                ],
            },
        ]
    )

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=300,
    )

    reply = response.choices[0].message.content

    chat_placeholder = st.markdown(reply)

    # # Continually update the chat component with chat messages
    # for message in messages:
    #     chat_placeholder.markdown(message['content'][0]['text'] if message['content'][0]['text'] else 'image')