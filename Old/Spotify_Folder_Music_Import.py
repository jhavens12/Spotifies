from pprint import pprint
import functions
from datetime import datetime
from os import listdir
from os.path import isfile, join
from collections import defaultdict
import csv

time = datetime.now()

mypath = '/Users/Havens/Dropbox/Spotify_Playlists/'

def create_spotify_search_dictionary(myfile):

    missing_list = []
    track_list = []
    columns = defaultdict(list)
    with open(mypath+myfile) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            for (i,v) in enumerate(row):
                columns[i].append(v)
    for n,current_track in enumerate(columns[0]):
        if "spotify:local" not in current_track:
            track_list.append(current_track)
        else:
            data = str(columns[2][n])+" "+str(columns[1][n])
            term_2 = data.replace('(', '').replace(')', '')
            term_3 = term_2.replace('&', '').replace('feat.', '')
            track = functions.track_search(term_3)
            if track != '':
                pass
            if track != []:
                pass
            if track != False:
                pass
            # if "NOT FOUND" in track:
            #     pass
            else:
                track_list.append(track)

    pprint(track_list)
    return track_list

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
file_dictionary = {}
for n,file in enumerate(sorted(onlyfiles)):
    c = n+1
    file_dictionary[c] = file

#extended_tracks = extended_playlist_search(token)
playlist_name = 'STARRED'
exclusion_p1 = [playlist_name]
exclusion_p2 = functions.exclusion_terms()
exclusion_list = exclusion_p1 + exclusion_p2

while True:
    pprint(file_dictionary)
    print()
    choice = int(input("What is the file number? "))
    print(file_dictionary[choice])
    track_list = create_spotify_search_dictionary(file_dictionary[choice])
    functions.add_to_playlist(functions.playlist_creation(playlist_name), track_list, exclusion_list)

    print()
    print()
