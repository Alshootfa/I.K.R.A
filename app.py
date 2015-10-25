from flask import Flask, url_for, redirect, request, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from model import *
from werkzeug import secure_filename

import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])

if not os.path.exists('data/media'):
    os.makedirs('data/media')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/media'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)

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
    courses = Course.query.all()
    return render_template('list_courses.html', courses=courses)

@app.route('/courses/<course_id>/media/add', methods=['GET', 'POST'])
def add_media(course_id):
    if request.method == 'POST':
        file = request.files['file']
        if not file or not is_allowed_file(file.filename):
            redirect('/courses/<course_id>/media/add', course_id=course_id)

        upload_media(course_id, file)
        return redirect(url_for('get_course', course_id=course_id))

    course = Course.query.filter_by(ID=course_id).first()
    return render_template('add_media.html', course=course)

def get_courses_dir(course_id):
    result = os.path.join('courses', course_id)
    try:
        os.makedirs(result)
    except OSError:
        pass
    return result

@app.route('/courses/<course_id>')
def get_course(course_id):
    course = Course.query.filter_by(ID=course_id).first()
    media = Media.query.filter_by(course_id=course_id)
    return render_template('course.html', course=course, media=media)

@app.route('/courses/<course_id>/media/<name>')
def get_media(course_id, name):
    media = Media.query.filter_by(course_id=course_id, name=name).first()
    return send_from_directory(app.config['UPLOAD_FOLDER'], media.location)

def upload_media(course_id, file):
    filename = secure_filename(file.filename)
    new_media = Media(course_id, filename, -1, None, get_file_extension(filename))
    new_media.location = os.path.join(get_courses_dir(course_id), filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_media.location))

    db.session.add(new_media)
    db.session.commit()

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1]

def is_allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

    with app.app_context():
        db.drop_all()
        db.create_all()

        # sample data
        sample_courses = [
            Course('basic math', 'how to add and stuff', 'basic.png'),
            Course('algebra', 'algebra and stuff', 'algebra.png')
        ]
        for course in sample_courses:
            db.session.add(course)
        upload_media(1, open('samples/adding_pt1.png'))
        upload_media(1, open('samples/adding_pt2.png'))
        upload_media(1, open('samples/adding_pt3.png'))
        upload_media(2, open('samples/adding_pt1.png'))
        upload_media(2, open('samples/adding_pt2.png'))
        db.session.commit()
