from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

@app.route('/')
@login_required
def index():
    print("Rendering index.html template...")
    return render_template('index.html')
    
if __name__ == '__main__':
         app.run(debug=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a real secret key
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=False)
    songlength = db.Column(db.Integer,nullable=False)

    # Add more fields as needed
    # notes field for users

with app.app_context():
    db.create_all()

#Add routes in app.py for adding, viewing, updating.CRUD 
# Create: Add a new song
@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        new_song = Song(title=title, artist=artist)
        db.session.add(new_song)
        db.session.commit()
        return redirect(url_for('view_songs'))
    return render_template('add_song.html')

# Read: View all songs
@app.route('/')
def view_songs():
    songs = Song.query.all()
    return render_template('view_songs.html', songs=songs)

# Update: Edit a song
@app.route('/edit_song/<int:id>', methods=['GET', 'POST'])
def edit_song(id):
    song = Song.query.get_or_404(id)
    if request.method == 'POST':
        song.title = request.form['title']
        song.artist = request.form['artist']
        db.session.commit()
        return redirect(url_for('view_songs'))
    return render_template('edit_song.html', song=song)

# Delete: Remove a song
@app.route('/delete_song/<int:id>')
def delete_song(id):
    song = Song.query.get_or_404(id)
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('view_songs'))

# Below is all about user/login functions 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('index'))