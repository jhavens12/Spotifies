from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import functions as f
import pprint

tt = f.top_tracks() #get dictionary of top track lists from Spotify
for x in tt:

    playlist_id = f.playlist_creation(x) #create playlist with name defined in f.top_tracks
    current = f.playlist_tracks(playlist_id) #get the current tracks in the playlist
    add_list = []
    remove_list = []

    for track in tt[x]: #for track in new list
        if track not in current:
            add_list.append(track) #add the track to be added

    for track in current: #for track in current list
        if track not in tt[x]:
            remove_list.append(track)

    if add_list:
        print("add_list")
        pprint.pprint(add_list)
        print("*****")
        print('Adding songs to Saved for you boss!')
        f.add_to_saved(add_list)
        f.add_to_playlist(playlist_id,add_list,[])
    if remove_list:
        print("remove_list")
        pprint.pprint(remove_list)
        print("*****")
        f.remove_from_playlist(playlist_id,remove_list)
    print("/////")
    print()
