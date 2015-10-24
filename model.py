from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    icon = db.Column(db.String(100))

    media = db.relationship("Media", backref="Course")

    def __init__(self, course_name, description, icon):
        self.course_name = course_name
        self.description = description
        self.icon = icon

class Media(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.ID'))
    name = db.Column(db.String(50))
    size = db.Column(db.Integer)
    location = db.Column(db.String(200))
    filetype = db.Column(db.String(100))

    def __init__(self, course_id, name, size, location, filetype):
        self.course_id = course_id
        self.name = name
        self.size = size
        self.locaton = location
        self.filetype = filetype
