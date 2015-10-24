from flask import Flask, url_for, redirect, request, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from model import *
from werkzeug import secure_filename

import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/media'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

with app.app_context():
    db.init_app(app)
    db.create_all()
    db.session.commit()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/math/square/<value>")
def show_math(value):

    value = square(value)

    return render_template('math.html', value=value)

def square(x):
    square = int(x) * int(x)
    return square

@app.route('/courses')
def list_courses():
	# course_name, description, icon
    courses = [
        Course('basic math', 'how to add and stuff', 'basic.png'),
        Course('algebra', 'algebra and stuff', 'algebra.png')
    ]
    return render_template('list_courses.html', courses=courses)

@app.route('/courses/<course_id>/media/add', methods=['GET', 'POST'])
def add_media(course_id):
    if request.method == 'POST':
        name = request.form['name']
        # file = request.files['file']
        # if not file or not is_allowed_file(file.filename):
        #     redirect('/media/add')

        # course_dir = os.path.join(app.config['UPLOAD_FOLDER'], 

        # filename = secure_filename(file.filename)
        # new_media = Media(-1, request.form['name'], -1, None, get_file_extension(filename)) 

        # new_media.location = os.path.join(new_media.name, filename)
        # upload_path = os.path.join(app.config['UPLOAD_FOLDER'], new_media.location)
        # try:
        #     os.makedirs(upload_path)
        # except IOError:
        #     pass
        # file.save(upload_path)

        # db.session.add(new_media)
        # db.session.commit()
        return redirect(url_for('get_media', name=name))

    return render_template('add_media.html')

@app.route('/media')
def list_media():
    # media = Media.query.all()
    media = [
        Media(123, 'how to add part 1', 242, '/courses/123/adding_pt1.mp4', 'mp4'),
        Media(123, 'how to add part 2', 243, '/courses/123/adding_pt2.mp4', 'mp4'),
        Media(123, 'how to add part 3', 244, '/courses/123/adding_pt3.mp4', 'mp4')
    ]
    return render_template('list_media.html', media=media)

@app.route('/media/<name>')
def get_media(name):    
    media = Media.query.filter_by(name=name).first()
    return send_from_directory(app.config['UPLOAD_FOLDER'], media.location)

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1]

def is_allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
