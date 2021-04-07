import os, datetime, json
from flask import Flask, flash, request, redirect, url_for, render_template, make_response


# UPLOAD_FOLDER = "D:\hempreport\static\photos"
UPLOAD_FOLDER = "static/photos/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        # description = request.form['description']
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        description = request.form["description"]
        temp = request.form["temp"]
        humidity = request.form["humidity"]
        photo = request.files["photo"]
        
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
        photo_name = photo.filename

        try:
            file = open("today.json")
            report = json.load(file)
            counter = int(max(report))
            report[counter + 1] = [date, description, temp, humidity, photo_name]
            file.close()

        except FileNotFoundError:
            report = {}
            file = open("today.json", 'w')
            report[1] = [date, description, temp, humidity, photo_name]
            file.close()

        file = open("today.json", 'w')
        json.dump(report, file)
        file.close()

        return redirect('/view')
    else:
        return render_template('upload.html')


@app.route('/view')
def view():

    try:

        file = open("today.json")
        report = json.load(file)

        sorted_keys_list = sorted(report, reverse=True)
        sorted_report = {}

        for k in sorted_keys_list:
            sorted_report[k] = report[k]

        return render_template('view.html', report=sorted_report)

    except:
        
        return render_template('view.html', report=None)


if __name__ == '__main__':
    app.run(debug=True)
    
    
