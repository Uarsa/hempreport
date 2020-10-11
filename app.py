import os, datetime, json
from flask import Flask, flash, request, redirect, url_for, render_template, make_response
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "D:\hempreport\static\photos"
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
        info = request.form["info"]
        photo = request.files["file"]
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
        # file.save(os.path.join('D:\\', 'files', 'photos'), file.filename)
        
        try:
            file = open('today.json') 
            report = json.load(file)
            counter = int(max(report))
            report[counter+1] = [date, info, photo]
            file.close()
        
        except FileNotFoundError:
            report = {}
            file = open(filename, 'w')
            report[1] = [date, info, photo]   # 0=date, 1=info, 2=photo
            file.close()
    
        file = open(filename, 'w')
        json.dump(report, file)
        file.close()
        
        return redirect('/view')
    else:
        return render_template('upload.html')



@app.route('/view')
def view():
    # image = os.path.join(app.config['UPLOAD_FOLDER'])
    # photo = os.path.join(app.config['UPLOAD_FOLDER'], 'face.jpg')
    # photo_name = r"static\photos\face.PNG"

    file = open('today.json')
    report = json.load(file)
    
    sorted_report = sorted(report, reverse=True)
    
    # return render_template('view.html', photo=photo_name, info=info, date=date)
    return render_template('view.html', report=sorted_report)





if __name__ == '__main__':
    app.run(debug=True)
    
    
  
