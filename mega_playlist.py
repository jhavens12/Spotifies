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
from pprint import pprint
import functions

mega_playlist = "Ultimate"

user_playlists = functions.get_user_playlists()

#Generate possible playlists to seach
q = ['Q1','Q2','Q3','Q4']
y = list(range(2010,2051,1))
names = []
for r in q:
    for s in y:
        names.append(str(s)+" "+r)

#Find the actual playlists that exist
pl_actual = {}
for pl_name in names: #for the names we just made
    for user_pl_name in user_playlists: #for the actual playlists that exist
        if pl_name == user_pl_name: #if they match
            pl_actual[pl_name] = user_playlists[user_pl_name] #append ID to list

#find ID of mega playlist
pl_id = functions.playlist_creation(mega_playlist) #get mega playlist

#add songs from each baby playlist to mega playlist using exclusions
for playlist_id in sorted(pl_actual.keys()): # for reach yearly playlist
    print("Getting songs from: "+str(playlist_id))
    exclusion_list = functions.playlist_tracks(pl_id) #songs already in mega playlist
    track_list = functions.playlist_tracks(pl_actual[playlist_id])
    functions.add_to_playlist(pl_id,track_list,exclusion_list)

print("Done")
