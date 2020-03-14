from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import pprint
import sys
import os
import subprocess
import spotipy.util as util
import credentials
from datetime import datetime

time = datetime.now()
print (time.date())
#timestamp = " "+str(time.year) +"/"+ str(time.month)+"/"+ str(time.day) #str(time.time().strftime('%I:%M %p'))
timestamp = str(time.date())
username = credentials.username

test_playlist_id = '1c9VYSNgfXYtH5y2DjWFuQ'

#scope = 'user-top-read'
scope = 'user-top-read user-library-read playlist-read-private playlist-modify-public playlist-modify-private user-library-modify'
token = util.prompt_for_user_token(username,scope,client_id=credentials.client_id,client_secret=credentials.client_secret,redirect_uri=credentials.redirect_uri)

def term_tracks(token, playlist_id, playlist_offset): #takes playlist ID and returns results

    term_dict = {}
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    ranges = ['short_term', 'medium_term', 'long_term']
    for range in ranges:
        #term_dict[range] = {}
        term_dict[range] = []
        results = sp.current_user_top_tracks(time_range=range, limit=10)
        for i, item in enumerate(results['items']):
            #w = i + 1
            #term_dict[range][w] = item['id']
            term_dict[range].append(item['id'])
    return term_dict

def playlist_creation(username,token,playlist_name):
    if playlist_name == 'short_term':
        title = "TT Short Term "+timestamp
    if playlist_name == 'medium_term':
        title = "TT Medium Term "+timestamp
    if playlist_name == 'long_term':
        title = "TT Long Term "+timestamp
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlists = sp.user_playlist_create(username,title,True)
        return playlists['id']
    else:
        print("Can't get token for", username)

def add_to_playlist(username,playlist_id,tracks,token):

    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, playlist_id, tracks)


top_tracks_dict = term_tracks(token, test_playlist_id, 0)
for x in top_tracks_dict:
    playlist_id = playlist_creation(username,token,x)
    add_to_playlist(username,playlist_id,top_tracks_dict[x],token)
