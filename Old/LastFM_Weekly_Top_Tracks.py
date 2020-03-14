from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import pprint
import sys
import os
import subprocess
import spotipy.util as util
import credentials
import last_fm_credentials
from datetime import datetime
import requests

time = datetime.now()
timestamp = " "+str(time.date())

last_fm_key = last_fm_credentials.key
last_fm_user = last_fm_credentials.user

#period (Optional) : overall | 7day | 1month | 3month | 6month | 12month - The time period over which to retrieve top tracks for.

dates = ["7day"]
DNS = ""

username = credentials.username

scope = 'user-library-read playlist-read-private playlist-modify-public playlist-modify-private user-library-modify'
token = util.prompt_for_user_token(username,scope,client_id=credentials.client_id,client_secret=credentials.client_secret,redirect_uri=credentials.redirect_uri)

def get_lastfm_tracks(input_period):

    url = "http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user="+last_fm_user+"&api_key="+last_fm_key+"&limit=25&period="+input_period+"&format=json"
    dataset = requests.get(url).json()
    dict_1 = {}
    for n,i in enumerate(dataset['toptracks']['track']):
        s = n+1
        dict_1[s] = {}
        dict_1[s]['artist'] = i['artist']['name']
        dict_1[s]['track'] = i['name']
    return dict_1

def spotify_search(term):
    search_term = term + DNS
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    result = sp.search(search_term, limit=1, type='track', market='US')
    if result['tracks']['total'] != 0:
        result_title = result['tracks']['items'][0]['name']
        result_artist = result['tracks']['items'][0]['artists'][0]['name']
        result_id = result['tracks']['items'][0]['id']
        # print("Search Term: "+search_term)
        # print("Result: "+result_artist+" "+result_title)
        # print()
        return result_id
    else:
        # print ("Search Term: "+search_term)
        # print ("NOT FOUND")
        # print()
        return str("NOT FOUND: " + search_term)

def playlist_creation(playlist_name):

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlists = sp.user_playlist_create(username,playlist_name,public=False)
        return playlists['id']
    else:
        print("Can't get token for", username)

def add_to_playlist(playlist_id,track_ids):

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        print(results)
    else:
        print("Can't get token for", username)

for current_date in dates:

    result_dict = get_lastfm_tracks(current_date)
    plist_id = playlist_creation(current_date+timestamp)
    track_list = []
    missing_list = []
    for x in result_dict:

        track = spotify_search(str(result_dict[x]['artist'])+" "+str(result_dict[x]['track']))
        if "NOT FOUND" in track:
            missing_list.append(track)
        else:
            track_list.append(track)

    pprint.pprint(missing_list)
    add_to_playlist(plist_id,track_list)


print ("DONE!")







    #
