
from flask import Flask, send_from_directory

import markdown

app = Flask(__name__)

@app.route('/')
def index():
    instructions = []
    with open("instructions.txt", "r") as file:
        instructions = file.readlines()


    instructions = ''.join(instructions)
    html_instructions = markdown.markdown(instructions)


    return f'<head><meta http-equiv="refresh" content="1"><link rel="stylesheet" href="https://unpkg.com/@thesephist/paper.css/dist/paper.min.css" /></head><body>{html_instructions}</body>'

app.run(port=5002)