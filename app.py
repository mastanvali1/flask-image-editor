from flask import Flask, render_template, request, flash, url_for, redirect, session
from werkzeug.utils import secure_filename
import cv2
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cwebp": 
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg": 
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng": 
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename
    pass

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['Username']
        password = request.form['Password']
    
        # Here you can implement your own authentication logic
        if username == 'mastan' and password == 'mastan@2024':
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))  # Redirect to login page if login fails
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/")
def home():
    if 'username' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('login'))

@app.route("/about")
def about():
    if 'username' in session:
        return render_template("about.html")
    else:
        return redirect(url_for('login'))

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if 'username' in session:
        if request.method == "POST": 
            operation = request.form.get("operation")
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return "error"
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return "error no selected file"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new = processImage(filename, operation)
                flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
                return render_template("index.html")

        return render_template("index.html")
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    
