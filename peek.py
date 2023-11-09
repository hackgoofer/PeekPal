from packaging import version
import pyautogui
import time
import datetime

# Your existing interval and screenshot functions here...

# Check the Pillow version to avoid the TypeError in pyscreeze
import pyscreeze
import PIL

__PIL_TUPLE_VERSION = tuple(int(x) for x in PIL.__version__.split("."))
pyscreeze.PIL__version__ = __PIL_TUPLE_VERSION

# Set the interval between screenshots in seconds
interval = 1  # e.g., 5 seconds

# Set the number of screenshots to take
number_of_screenshots = 200


# Function to take a screenshot
def take_screenshot():
    # Get the current time in a readable format
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # Set the filename with the current timestamp
    filename = f"screenshots/screenshot_{timestamp}.png"
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    # Save the screenshot
    screenshot.save(filename)
    print(f"Screenshot taken and saved as {filename}")


# Main loop to take screenshots at the given interval
for _ in range(number_of_screenshots):
    take_screenshot()
    # Wait for the specified interval
    time.sleep(interval)

print("Done taking screenshots.")
