from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from model import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
