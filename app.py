import json
from datetime import datetime
from flask import Flask, flash, request, redirect, url_for, render_template, make_response


UPLOAD_FOLDER = "static/photos/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# counting bush number. contains zero when created.
def counter():
    with open("static/resource/number_list.txt", "r") as f:
        i = f.read()
        count = int(i)
        return count


@app.route('/')
@app.route('/home')
def index():
    count = counter()
    return render_template('index.html', count=count)
  
  
