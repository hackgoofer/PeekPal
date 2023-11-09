from openai import OpenAI
import base64
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


messages = [
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
                "image_url": {
                    "url": f"data:image/png;base64,{encode_image('screenshots/spotify.png')}"
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=messages,
    max_tokens=300,
)

reply = response.choices[0]
print("1111111")
print(reply)

messages.extend(
    [
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": reply.message.content,
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "According to the screenshot, what is the next step so that I can listen to the same song at the same time with a friend?",
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

reply = response.choices[0]
print("222222")
print(reply)


messages.extend(
    [
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": reply.message.content,
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encode_image('screenshots/spotify2.png')}"
                    },
                },
                {
                    "type": "text",
                    "text": "I got to this step, now what?",
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

reply = response.choices[0]
print("33333")

print(reply)
