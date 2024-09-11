# importing necessary modules
from flask import Flask, redirect, request, jsonify
import requests
import base64
import json
import csv
from urllib.parse import urlencode

"""
# creates playlist array from csv

def csv_to_array(file_path):
    data_array = []
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data_array.append(row)
    return data_array

csv_file_path = 'simmering_data.csv'
csv_data_array = csv_to_array(csv_file_path)

# Extracting track names and artists separately
track_names = [row[0] for row in csv_data_array[1:]]
artists = [row[1] for row in csv_data_array[1:]]

# Combining track names and artists into a list of dictionaries
source_playlist = [{"track_name": track_name, "artist": artist} for track_name, artist in zip(track_names, artists)]
print(source_playlist)
playlist_name  = "simmering"
"""

# Spotify API endpoints
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
SPOTIFY_CREATE_PLAYLIST_URL = SPOTIFY_API_BASE_URL + "/users/{user_id}/playlists"
SPOTIFY_SEARCH_TRACK_URL = SPOTIFY_API_BASE_URL + "/search"

# Spotify app credentials
CLIENT_ID = "86f97353dea1489287c4ff55cc479cdb"
CLIENT_SECRET = "73ac6aaf0c5e4103b7a7bbc1bfaf80a9"
REDIRECT_URI = "http://localhost:5000/callback"

from musi_scraper import source_playlist, playlist_name
print(source_playlist, playlist_name)

app = Flask(__name__)

@app.route("/")
def index():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=playlist-modify-private"
    return redirect(auth_url)      

@app.route("/callback")
def callback():
    code = request.args.get("code")
    access_token = get_access_token(code)
    if access_token:
        user_id = get_user_id(access_token)
        playlist_id = create_spotify_playlist(access_token, user_id, playlist_name)
        if playlist_id:
            for track_info in source_playlist:
                track_uri = search_spotify_track(access_token, track_info["track_name"], track_info["artist"])
                if track_uri:
                    add_track_to_playlist(access_token, playlist_id, track_uri)
                else:
                    print(f"Track '{track_info['track_name']}' by '{track_info['artist']}' not found on Spotify.")
            return "Playlist created successfully!"
        else:
            return "Failed to create playlist."
    else:
        return "Failed to obtain access token."

def get_access_token(code):
    # Exchange authorization code for access token
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(token_url, headers=headers, data=urlencode(data))
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def get_user_id(access_token):
    # Get the user's Spotify ID
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY_API_BASE_URL + "/me", headers=headers)
    if response.status_code == 200:
        return response.json()["id"]
    return None


def create_spotify_playlist(access_token, user_id, playlist_name):
    # Create a new playlist on Spotify
    create_playlist_url = SPOTIFY_CREATE_PLAYLIST_URL.format(user_id=user_id)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "name": playlist_name,
        "public": False  # can set it to True if you want it to be public
    })
    response = requests.post(create_playlist_url, headers=headers, data=data)
    if response.status_code == 201:
        return response.json()["id"]
    return None

# consider using different configurations for the query for improving accuracy
# artist can be specificied but tracks will not be found more often
# check https://developer.spotify.com/documentation/web-api/reference/search for more specifics
def search_spotify_track(access_token, track_name, artist):
    # search for a track on Spotify
    params = {
        "q": f"{track_name + artist}",
        "type": "track",
        "limit": 1
    }
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY_SEARCH_TRACK_URL, headers=headers, params=params)
    if response.status_code == 200:
        items = response.json()["tracks"]["items"]
        if items:
            return items[0]["uri"]  # Return the Spotify URI of the first search result
    return None

def add_track_to_playlist(access_token, playlist_id, track_uri):
    # Add a track to a Spotify playlist
    add_track_url = f"{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "uris": [track_uri]
    })
    response = requests.post(add_track_url, headers=headers, data=data)
    return response.status_code == 201

if __name__ == "__main__":
    app.run(debug=True)