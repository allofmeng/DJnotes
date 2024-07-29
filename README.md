# DJnotes
#### Video Demo:  (https://youtu.be/56tbK4eMN28)
#### Description:
DJnotes is a web application that allows DJs to manage their song lists, add notes, and organize their music library.
In the project you will find some key files, first is app.py, this is where I wrote the main part of my python operation , you can find login , logout , register , index and my database set up in there. 
If you move on to src.main , in it you will find some python functions that was part of testing on how to fetch song in from spotify website, my first try was url_reader.py (also songinforeader.py) which was to parse html and find the right og elements , but it was too unstable so I didn't use it. 
Then I moved on to try spotify api instead, with the help of Claude sonnet's guidance , I was able to create a developer account and use api keys to fetch song info using track url. This is proven to be more stable and easier to handle thus I decided to use in final design. 
Thank you for your time reading this , looking forward to hear your comments. 


## Features

- User authentication (login/logout)
- Add songs from Spotify
- Edit song details (title, artist, album, length)
- Add personal notes to songs
- View all songs in a table format
- Responsive design for mobile and desktop use

## Technologies Used

- Flask: Web framework
- SQLAlchemy: ORM (Object Relational Mapper)
- Flask-Login: User session management
- Spotify API: For fetching song information
- Bootstrap: Front-end framework
- JavaScript: For dynamic content updates

## Setup and Installation

1. Clone the repository:
git clone https://github.com/allofmeng/DJnotes.git
cd djnotes
2. Set up a virtual environment:
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
3. Install the required packages:
pip install -r requirements.txt
4. Set up environment variables:
Create a `.env` file in the root directory and add the following:
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///djnotes.db
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
5. Initialize the database:
flask db upgrade
6. Run the application:
7. Open a web browser and navigate to `http://localhost:5000`

## Usage

1. Register a new account or log in to an existing account.
2. Add songs by pasting a Spotify URL into the "Add Song" form.
3. View your songs in the table on the main page.
4. Click "Edit" to modify song details or add notes.
5. Click "Delete" to remove a song from your list.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Mozilla license, see the license branch for details. 

## Acknowledgments
- This project is coded with the help of online resources which includes Claude 3.5. 
- Thanks to Spotify for providing the API to fetch song information.
- Bootstrap for the responsive design components.
- Thanks to G.Kiff for the guidance and time to teach me.