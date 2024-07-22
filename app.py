from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

@app.route('/')
def home():
         return render_template('index.html')

if __name__ == '__main__':
         app.run(debug=True)




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=False)

    # Add more fields as needed
    # notes field for users

with app.app_context():
    db.create_all()

#Add routes in app.py for adding, viewing, updating, and 