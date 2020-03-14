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
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from os import listdir
from os.path import isfile, join
import csv
from collections import defaultdict
import math
import functions

uri = sys.argv[1]

if "spotify:user:" in uri:
    playlist_username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]
elif "https://open.spotify.com/user" in uri:
    playlist_username = uri.split('/')[4]
    playlist_id_full = uri.split('/')[6]
    playlist_id = playlist_id_full.split('?')[0]


track_list = functions.playlist_tracks(playlist_id)
track_dict = functions.track_info_search(track_list)

id_list = []
dup_list = []
for track in track_dict:
    id = track_dict[track]['id']
    if id not in id_list:
        id_list.append(id)
    else:
        dup_list.append(id)

pprint(dup_list)

functions.remove_from_playlist(playlist_id,dup_list)
