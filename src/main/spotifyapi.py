from flask import Flask, jsonify, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
from urllib.parse import urlparse

# Initialize the Flask app


# Spotify API credentials
CLIENT_ID = '6e7465ad19ce4909a26c666dd8632442'
CLIENT_SECRET = '379b979870474805946a4308beac0a51'

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def add_song(url: str) -> dict:
    try:
        # Extract track ID from URL
        track_id = url.split('/')[-1].split('?')[0]

        # Fetch track information
        track_info = sp.track(track_id)

        # Extract relevant information
        title = track_info['name']
        album = track_info['album']['name']
        artist = track_info['artists'][0]['name']
        length = track_info['duration_ms']

        return {
            'title': title,
            'album': album,
            'artist': artist,
            'length': length,
            'message': 'Song information retrieved successfully'
        }

    except Exception as e:
        raise Exception(f"Error processing song: {str(e)}")


