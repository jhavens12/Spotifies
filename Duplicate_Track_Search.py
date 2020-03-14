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
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from os import listdir
from os.path import isfile, join
import csv
from collections import defaultdict
import math
import functions

playlist_list = functions.get_user_playlists()
playlist_dict = {}

for n,playlist in enumerate(sorted(playlist_list)):
    c = n+1
    playlist_dict[c] = playlist

pprint(playlist_dict)
choice = int(input("What is the file number? "))
print(playlist_list[playlist_dict[choice]])

track_list = functions.playlist_tracks(playlist_list[playlist_dict[choice]])
track_dict = functions.track_info_search(track_list)

match_dict = {}
for track1 in track_dict:
    for track2 in track_dict:
        #print(track_dict[track1]['artist'])
        #print(track_dict[track2]['artist'])
        if track_dict[track1]['id'] != track_dict[track2]['id']: #weed out exact matches
            if track_dict[track1]['artist'][:3] == track_dict[track2]['artist'][:3]: #find if artist matches
                if track_dict[track1]['title'][:3] == track_dict[track2]['title'][:3]:
                    # print ("MATCH")
                    # print(track_dict[track1]['artist']+" "+track_dict[track1]['title']+" "+track_dict[track1]['album'])
                    # print(track_dict[track2]['artist']+" "+track_dict[track2]['title']+" "+track_dict[track2]['album'])
                    # print()
                    match_dict[track_dict[track1]['id']] = {}
                    match_dict[track_dict[track1]['id']] = track_dict[track1]
                    match_dict[track_dict[track2]['id']] = {}
                    match_dict[track_dict[track2]['id']] = track_dict[track2]
                else:
                    pass
            else:
                pass
        else:
            pass
#pprint(match_dict)
choice_dict = {}
for n,track in enumerate(match_dict):
    c = n+1
    choice_dict[c] = match_dict[track]
    print(str(c)+": "+match_dict[track]['artist']+" - "+match_dict[track]['title']+" - "+match_dict[track]['album'])

if not match_dict:
    print("No matches found. Goodbye")
else:
    user_input = input("Enter three numbers separated by commas: ")

    input_list = user_input.split(',')
    numbers = [int(x.strip()) for x in input_list]

    remove_list = []
    for number in numbers:
        remove_list.append(choice_dict[number]['id'])

    print("Remove List")
    pprint(remove_list)
    #pprint(choice_dict)


    functions.remove_from_playlist(playlist_list[playlist_dict[choice]],remove_list)
