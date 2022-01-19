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

        file = open("plants.json")   # main dict
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
            file = open("plants.json")   # dict inside
            plants = json.load(file)
            counter_main = int(max(plants))
            plants[counter_main + 1] = [name, description, photo_name, date]
            file.close()
            # creates a file into which data will be written further
            bush_name = str(counter_main + 1) + ".json"
            # create an empty dict with all plant data, which will be filled further
            plant_data = {}
            with open(bush_name, "w") as f:
                json.dump(plant_data, f)
            
        except FileNotFoundError:
            # create list with plants main info. for preview on main page
            plants = {}
            file = open("plants.json", 'w')   # create file
            plants[1] = [name, description, photo_name, date]   # first writing
            file.close()
            # create a first file of the fisrt bush, into which data will be written further
            bush_name = "1.json"
            # create an empty dict with all first plant data, which will be filled further
            plant_data = {}
            #plant_data = {1:["03.09.2021", "start growing", "28", "55"], 2:["04.09.2021", "normal mode", "30", "60"]}
            with open(bush_name, "w") as f:
                json.dump(plant_data, f)

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
        sorted_plant_data = {}
        with open(bush_name) as f:
            plant_data = json.load(f)   # dict
        sorted_keys_list = sorted(plant_data, reverse=True)
        for k in sorted_keys_list:
            sorted_plant_data[k] = plant_data[k]
        bush_id = id   
        return render_template('view.html', bush=current_bush, report=sorted_plant_data, bush_id=bush_id)
    
    
    except:
        pass
    
    
    
    
@app.route('/add_post/<int:id>', methods=['POST', 'GET'])
def add_post(id):
    return render_template('add.html')
        
    

    
    
    
    
'''   
# norm    
@app.route('/add_post/<int:id>', methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        description = request.form["description"]
        temp = request.form["temp"]
        humidity = request.form["humidity"]
        photo = request.files["photo"]
        
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
        photo_name = photo.filename

        
        bush_name = str(id) + ".json"
        
        with open(bush_name) as f:
            plant_data = json.load(f)
            
        plant_data["1"] = [date, description, temp, humidity]
        
        with open(bush_name, "w") as f:
            json.dump(plant_data, f)
            
        return redirect('/view')
    
    
    else:
        return render_template('add_post.html')   

''' 
'''        
@app.route('/add_post/<int:id>', methods=['POST', 'GET'])
def add_post():
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
    


    
if __name__ == '__main__':
    app.run(debug=True)

    
    
