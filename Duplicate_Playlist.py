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
timestamp = " "+str(time.date())

uri = sys.argv[1]

if "spotify:user:" in uri:
    playlist_username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]
elif "https://open.spotify.com/user" in uri:
    playlist_username = uri.split('/')[4]
    playlist_id_full = uri.split('/')[6]
    playlist_id = playlist_id_full.split('?')[0]

print(playlist_username)
print(playlist_id)
#user spotify username
username = credentials.username

#auth token for modify requests
scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username,scope,client_id=credentials.client_id,client_secret=credentials.client_secret,redirect_uri=credentials.redirect_uri)

def playlist_info(playlist_username, playlist_id, token):
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist(playlist_username, playlist_id)

    playlist_track_count = results['tracks']['total']
    playlist_name = results['name']
    if 'display_name' in results['owner']:
        playlist_owner = results['owner']['display_name']
    else:
        playlist_owner = results['owner']['id']

    return playlist_owner, playlist_name, playlist_track_count

def playlist_track_info(playlist_username, playlist_id, playlist_offset, token):
    playlist_songs = []
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_tracks(playlist_username, playlist_id, limit=100, offset=playlist_offset)
    if 'items' in results:
        for x in results['items']:
            if x['track'] != None:
                if x['track']['id'] == None:
                    print("Track ID is NONE")
                else:
                    playlist_songs.append(x['track']['id'])
            else:
                print("Track is missing information in playlist")
    return playlist_songs

def playlist_creation(username,playlist_name,token):

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlists = sp.user_playlist_create(username,playlist_name,True)
        return playlists['id']
    else:
        print("Can't get token for", username)

def add_to_playlist(username,playlist_id,track_ids,token):

    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    else:
        print("Can't get token for", username)

imported_playlist_owner, imported_playlist_name, imported_playlist_count = playlist_info(playlist_username, playlist_id, token)

if imported_playlist_owner != None:
    new_playlist_name = imported_playlist_owner +" - "+imported_playlist_name + timestamp
else:
    new_playlist_name = imported_playlist_name + timestamp

if imported_playlist_count < 100:
    new_playlist_id = playlist_creation(username,new_playlist_name,token)
    track_list = playlist_track_info(playlist_username, playlist_id, 0, token)
    #print(track_list)
    add_to_playlist(username,new_playlist_id,track_list,token)
    print("done")

else:
    print ("this playlist has "+str(imported_playlist_count)+" tracks")
    new_playlist_id = playlist_creation(username,new_playlist_name,token)
    offset = 0
    track_list = playlist_track_info(playlist_username, playlist_id, 0, token)
    add_to_playlist(username,new_playlist_id,track_list,token)
    while (len(track_list) < imported_playlist_count):
        offset = offset + 100
        track_list_part = playlist_track_info(playlist_username, playlist_id, offset, token)
        if track_list_part:
            #print(track_list_part)
            add_to_playlist(username,new_playlist_id,track_list_part,token)
            track_list = track_list+track_list_part

    print("done")
