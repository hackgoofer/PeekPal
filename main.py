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


def write_items_to_file(items, filename="instructions.txt"):
    with open(filename, "w") as file:
        # Write items in reverse order
        for item in reversed(items):
            file.write(f"### Todo added at time: {item[1]}\n")
            file.write(f"{item[0]}\n")
            file.write(f"\n\n\n")


def get_screenshot():
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
    return encoded_image


goal = "listen to the same song at the same time with a friend"
with open("goal.txt", "r") as file:
    goal = file.readline().strip()

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

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=messages,
    max_tokens=300,
)

reply = response.choices[0].message.content
print(reply)
replies.append((reply, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

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
replies.append((reply, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

while True:
    # Get all screenshot files

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
                        "image_url": {
                            "url": f"data:image/png;base64,{get_screenshot()}"
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

    reply = response.choices[0].message.content
    print(f"GPT replies: {reply}")
    replies.append((reply, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    write_items_to_file(replies)
    time.sleep(1)
