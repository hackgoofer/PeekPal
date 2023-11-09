import fal
from dotenv import load_dotenv

load_dotenv()

handler = fal.apps.submit(
    "110602490-whisper",
    arguments={"url": "https://cdn.freesound.org/previews/324/324783_5589643-lq.mp3"},
)

for event in handler.iter_events():
    if isinstance(event, fal.apps.InProgress):
        print("Request in progress")
        print(event)

result = handler.get()
print(result)
