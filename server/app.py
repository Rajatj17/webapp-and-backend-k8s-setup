from flask import Flask
from datetime import datetime

app = Flask(__name__)

def write_to_file(message):
        # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Format the text with the timestamp
    formatted_text = f'[{timestamp}] {message}\n'

    # Append the formatted text to the file
    with open('/data/persistent-file.txt', 'a') as file:
        file.write(formatted_text)

    return formatted_text

@app.route("/")
def hello_world():
    write_to_file('New message')
    return "<p>Hello, World!</p>"