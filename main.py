from openai import OpenAI
import base64
from dotenv import load_dotenv
import time
import os
import glob
import datetime

load_dotenv()

client = OpenAI()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def write_items_to_file(items, filename="what you should do.txt"):
    with open(filename, "w") as file:
        # Write items in reverse order
        for item in reversed(items):
            file.write(f"{item}\n")


goal = "listen to the same song at the same time with a friend"
with open("what i'm doing.txt", "r") as file:
    goal = file.readline().strip()

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
replies = []

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=messages,
    max_tokens=300,
)

reply = response.choices[0].message.content
print(reply)
replies.append(reply)

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
                    "text": f"According to the screenshot, what is the next step so to achieve the goal: {goal}",
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
print(reply)
replies.append(reply)

while True:
    # Get all screenshot files
    screenshot_files = glob.glob("screenshots/screenshot_*.png")
    screenshot_files = [screenshot.split(".")[0] for screenshot in screenshot_files]
    # Parse the timestamp from the filename and sort the files by timestamp
    sorted_screenshot_files = sorted(
        screenshot_files,
        key=lambda x: datetime.datetime.strptime(x.split("_")[1], "%Y-%m-%d-%H-%M-%S"),
        reverse=True,
    )
    # Get the second latest screenshot
    screenshot_to_parse = sorted_screenshot_files[1]
    print(f"parsing screenshot: {screenshot_to_parse}.png")
    encoded_image = encode_image(f"{screenshot_to_parse}.png")

    messages.extend(
        [
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": reply,
                    },
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{encoded_image}"},
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

    reply = response.choices[0].message.content
    print(f"GPT replies: {reply}")
    replies.append(reply)
    write_items_to_file(replies)
    time.sleep(2)
