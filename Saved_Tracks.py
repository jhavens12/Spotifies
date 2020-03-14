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

saved_remove_list = [] #create list of songs to remove from saved at end
track_dict = functions.user_saved_tracks() #generate saved track dictionary
for key in track_dict.keys():
  saved_remove_list.append(key) #add song ids to list to be removed

###
playlist_list = []
quarter_dict = {} #holds
for x in track_dict: #create dictionary of track id's and playlist names
    if 1 <= track_dict[x].month <= 3:
        quarter_dict[x] = str(track_dict[x].year)+" Q1"
    elif 4 <= track_dict[x].month <= 6:
        quarter_dict[x] = str(track_dict[x].year)+" Q2"
    elif 7 <= track_dict[x].month <= 9:
        quarter_dict[x] = str(track_dict[x].year)+" Q3"
    elif 10 <= track_dict[x].month <= 12:
        quarter_dict[x] = str(track_dict[x].year)+" Q4"

for x in quarter_dict: #create list of playlist names
    if quarter_dict[x] not in playlist_list:
        playlist_list.append(quarter_dict[x])
    #playlist_list.append(quarter_dict[x]) if quarter_dict[x] not in playlist_list except: pass

final_playlist_dict = {} #holds playlist names/ids

for x in playlist_list: #checks by name ex 2017 Q4, gets playlist IDS or creates them
    final_playlist_dict[x] = functions.playlist_creation(x)

plist_and_tracks = {}
for x in quarter_dict: #creates dictionary of playlist IDS as keys and track list as values
    #for each track in the quarter dict (track ID as key and playlist name as value)
    if final_playlist_dict[quarter_dict[x]] in plist_and_tracks: #if playlist id exists already, skip
        pass
    else:
        plist_and_tracks[final_playlist_dict[quarter_dict[x]]] = [] #else, create it
    plist_and_tracks[final_playlist_dict[quarter_dict[x]]].append(x) #then add track to appropriate list

exclusion_list = functions.exclusion_terms() #creates exclusion terms
for playlist in plist_and_tracks: #for each playlist, add associated track list
    functions.add_to_playlist(playlist,plist_and_tracks[playlist],exclusion_list)

if not saved_remove_list:
    print("0 songs to be moved and removed from saved")
else:
    print(str(len(saved_remove_list))+" songs to be removed from saved")
    functions.remove_from_saved(saved_remove_list)
