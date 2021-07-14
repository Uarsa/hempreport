import json
from datetime import datetime
from flask import Flask, flash, request, redirect, url_for, render_template, make_response


UPLOAD_FOLDER = "static/photos/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# mechanism of site.
# counting bush number. in beginning contains zero.
def counter():
    with open("static/resource/number_list.txt", "r") as f:
        i = f.read()
        count = int(i)
        return count
    
    
# mechanism of site.
# increase counter on one.
def counter_plus():
    with open("static/resource/number_list.txt", "r") as f:
        i = f.read()
        count = int(i)
        count = count + 1
        
    with open("static/resource/number_list.txt", "w") as f:
        f.write(str(count))
        
        
@app.route('/')
@app.route('/home')
def index():
    count = counter()
    return render_template('index.html', count=count)


@app.route('/new_plant', methods=['POST', 'GET'])
def new_plant():
    if request.method == 'POST':
        bush_number = str(counter())
        counter_plus()
        filename = bush_number + ".json"
        date = str(datetime.now().strftime("%d.%m.%Y"))
        name = request.form["name"]
        description = request.form["description"]
        photo = request.files["photo"]
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
        photo_name = photo.filename
        bush = [bush_number, name, description, photo_name, date]
        
        with open(filename, "w") as f:
            json.dump(bush, f)
            
        return redirect('/')
    
    else:
        return render_template('new_plant.html')







# for testing.
# increase count on one when press New plant button.
@app.route('/<int:count>')
def counts(count):
    try:
        counter_plus()
        return redirect('/')
    except:
        return "Something goes wrong..."
    
    
if __name__ == '__main__':
    app.run(debug=True)    
    
  
  




























