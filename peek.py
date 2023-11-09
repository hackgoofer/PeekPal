from packaging import version
import pyautogui
import time
import datetime
import os
import glob

# Your existing interval and screenshot functions here...

# Check the Pillow version to avoid the TypeError in pyscreeze
import pyscreeze
import PIL

__PIL_TUPLE_VERSION = tuple(int(x) for x in PIL.__version__.split("."))
pyscreeze.PIL__version__ = __PIL_TUPLE_VERSION

# Set the interval between screenshots in seconds
interval = 5  # e.g., 5 seconds

# Set the number of screenshots to take
number_of_screenshots = 2

# Directory to save screenshots
directory = "screenshots"


# Function to take a screenshot
def take_screenshot():
    # Get the current time in a readable format
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # Set the filename with the current timestamp
    filename = f"{directory}/screenshot_{timestamp}.png"
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    # Save the screenshot
    screenshot.save(filename)
    print(f"Screenshot taken and saved as {filename}")


# Function to delete old screenshots
def delete_old_screenshots():
    files = glob.glob(f"{directory}/*.png")
    files.sort(key=os.path.getmtime)
    print(files)
    # Delete all but the 20 most recent screenshots
    for file in files[:-number_of_screenshots]:
        os.remove(file)


# Main loop to take screenshots at the given interval
while True:
    take_screenshot()
    delete_old_screenshots()
    # Wait for the specified interval
    time.sleep(interval)

print("Done taking screenshots.")
