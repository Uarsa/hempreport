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
    try:

        file = open("plants.json")
        plants = json.load(file)
        sorted_keys_list = sorted(plants, reverse=True)
        sorted_plants = {}
        file.close()
        for k in sorted_keys_list:
            sorted_plants[k] = plants[k]
            
        return render_template('index.html', plants=sorted_plants)
    
    except:
        return render_template('index.html', plants=None)


@app.route("/new_plant", methods=['POST', 'GET'])
def new_plant():
    if request.method == 'POST':
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        name = request.form["name"]
        description = request.form["description"]
        photo = request.files["photo"]
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
        photo_name = photo.filename
        
        try:
            # dict with plants main info. for preview on main page
            file = open("plants.json")
            plants = json.load(file)
            counter_main = int(max(plants))
            plants[counter_main + 1] = [name, description, photo_name, date]
            file.close()
            # creates a file into which data will be written next
            bush_name = str(counter_main + 1) + ".json"
            # create empty dict with all plant's data which will be written next
            plant_data = {}
            with open(bush_name, "w") as f:
                plants_data[0] = []
            
        except FileNotFoundError:
            # create list with plants main info. for preview on main page
            plants = {}
            file = open("plants.json", 'w')
            plants[1] = [name, description, photo_name, date]
            file.close()
            # creates a first file into which data will be written
            bush_name = "1.json"
            # create empty dict with all plant's data which will be written next
            plant_data = {}
            with open(bush_name, "w") as f:
                plants_data[0] = []

        file = open("plants.json", 'w')
        json.dump(plants, file)
        file.close()

        return redirect('/')
    
    else:
        return render_template('new_plant.html')
    
    
    
@app.route('/view/<int:id>')
def view(id):
    try:
        file = open("plants.json")
        plants = json.load(file)   # dict
        current_bush = plants[str(id)]
        file.close()
        bush_name = str(id) + ".json"
        with open(bush_name) as f:
                pass
    
        return render_template('view.html', bush=current_bush, bush_name=bush_name)
    
    
    except:
        pass
    
    
        
        
        

        
        
        
        
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

    
'''
@app.route('/view/<int:id>')
def view(id):
    try:
        file = open("today.json")
        report = json.load(file)
        sorted_keys_list = sorted(report, reverse=True)
        sorted_report = {}
        file.close()

        for k in sorted_keys_list:
            sorted_report[k] = report[k]
            
        return render_template('view.html', report=sorted_report)

    except:
        
        return render_template('view.html', report=None)
'''   

    
if __name__ == '__main__':
    app.run(debug=True)

    
    
