import os
from flask import Flask, render_template, request
from image_processor import process_image
from text_processor import generate_response
import textwrap
from IPython.display import display
from IPython.display import Markdown
import pandas as pd


app = Flask(__name__)

# Get the current working directory
current_directory = os.getcwd()
#  create a folder named uploads in the current directory
os.makedirs(os.path.join(current_directory, 'uploads'), exist_ok=True)

UPLOAD_FOLDER = os.path.join(current_directory, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

@app.route("/")
def home():
    return render_template("index.html")

# Process uploaded image or generate response for text
@app.route("/chat", methods=["POST"])
def chat():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            image_info = process_image(filename)
            return image_info

    user_message = request.form["user_message"]
    bot_response = generate_response(user_message)
    #  use markdown to format the response
    # bot_response = to_markdown(bot_response)
    return bot_response

if __name__ == "__main__":
    app.run(debug=True)
