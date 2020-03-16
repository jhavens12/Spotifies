from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotipy
import credentials
from pprint import pprint
import math
from datetime import datetime

username = credentials.username
playlist_username = credentials.username #this is used to get my own playlists for some reason

#auth token for modify requests
#scope = 'playlist-modify-public'
scope = 'user-library-read playlist-read-private playlist-modify-public playlist-modify-private user-library-modify user-read-currently-playing user-read-playback-state user-modify-playback-state' #pulled from top tracks
token = util.prompt_for_user_token(username,scope,client_id=credentials.client_id,client_secret=credentials.client_secret,redirect_uri=credentials.redirect_uri)

def currently_playing():
    #gets currently playing track and returns track ID in list form (add to saved takes list)
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.current_user_playing_track()
    print("Currently Playing:")
    print()
    print(results['item']['artists'][0]['name'])
    print(results['item']['name'])
    #print(results['item']['id'])
    return_list = []
    return_list.append(results['item']['id'])
    return return_list

def playlist_info(playlist_username, playlist_id):
    #input is UUID of playlist and playlist_username
    #returns dictionary of information about playlist
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist(playlist_username, playlist_id)

    playlist_track_count = results['tracks']['total']
    playlist_name = results['name']
    if 'display_name' in results['owner']:
        playlist_owner = results['owner']['display_name']
    else:
        playlist_owner = results['owner']['id']

    return_dict = {}
    return_dict['playlist_owner_id'] = playlist_username
    return_dict['playlist_id'] = playlist_id
    return_dict['playlist_owner'] = playlist_owner
    return_dict['playlist_name'] = playlist_name
    return_dict['track_count'] = playlist_track_count

    return return_dict

def playlist_creation(playlist_name):
    #inputs playlist name (String)
    #checks to see if it exists
    #If yes: returns UUID
    #if no, creates playlist and returns UUID
    current_playlist_dict = get_user_playlists() #finds  current users playlists

    if playlist_name in current_playlist_dict: #check to see if playlist exists already
        print("Playlist name exists on Spotify: "+playlist_name)
        plist_id = current_playlist_dict[playlist_name] #if it does, grab ID
    else:
        print("Playlist name does not exist and will be created: "+playlist_name)
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        playlists = sp.user_playlist_create(username,playlist_name,public=False)
        plist_id = playlists['id']

    return plist_id

def get_playlist_id(playlist_name):
    #inputs playlist name (String)
    #returns uri if possible
    current_playlist_dict = get_user_playlists() #finds  current users playlists
    if playlist_name in current_playlist_dict: #check to see if playlist exists already
        print("Playlist name exists on Spotify: "+playlist_name)
        plist_id = current_playlist_dict[playlist_name] #if it does, grab ID
    else:
        plist_id = 0
    return plist_id

def get_my_current_quarter_playlist():
    timestamp = datetime.now()
    if 1 <= timestamp.month <= 3:
        playlist_name = str(timestamp.year) + " Q1"
    elif 4 <= timestamp.month <= 6:
        playlist_name = str(timestamp.year) + " Q2"
    elif 7 <= timestamp.month <= 9:
        playlist_name = str(timestamp.year) + " Q3"
    elif 10 <= timestamp.month <= 12:
        playlist_name = str(timestamp.year) + " Q4"
    return playlist_name

def playlist_tracks(playlist_id):
    #input is UUID of playlist
    #returns list of song ids
    track_ids = []
    playlist_dict = playlist_info(playlist_username, playlist_id)
    track_count = int(playlist_dict['track_count'])
    if track_count < 100:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_tracks(username, playlist_id, offset=0)
        for song in results['items']:
            track_ids.append(song['track']['id'])
    else:
        print("playlist "+playlist_dict['playlist_name']+" is "+str(track_count)+" tracks long")
        total_iterations = math.ceil(track_count/100)
        for count in range(0,total_iterations):
            print("Section: "+str(count+1)+" Of: "+str(total_iterations))
            the_offset = int(count*100) #finds wtrack numbers it needs
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            results = sp.user_playlist_tracks(username, playlist_id, offset=the_offset)
            for song in results['items']:
                track_ids.append(song['track']['id'])

    return track_ids

def track_info_search(track_ids):
    #input a list of track ids, get artist and title of each along with id

    result_dict = {}
    track_count = len(track_ids)
    if track_count < 50:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.tracks(track_ids)
        for n,result in enumerate(results['tracks']):
            c = n+1
            result_dict[c] = {}
            result_dict[c]['title'] = result['name']
            result_dict[c]['artist'] = result['artists'][0]['name']
            result_dict[c]['id'] = result['id']
            result_dict[c]['album'] = result['album']['name']
        return result_dict

    else:
        result_list = []

        list_of_lists = [track_ids[i:i+50] for i in range(0, len(track_ids), 50)]
        print("There are "+str(len(list_of_lists))+" sections to look up")
        for r,current_list in enumerate(list_of_lists):
            print("Section "+str(r+1)+" out of "+str(len(list_of_lists)))
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            results = sp.tracks(current_list)
            #result_big_dict.update(results)
            for n,result in enumerate(results['tracks']):
                c = n+1
                result_dict = {}
                result_dict[result['id']] = {}
                result_dict[result['id']]['title'] = result['name']
                result_dict[result['id']]['artist'] = result['artists'][0]['name']
                result_dict[result['id']]['id'] = result['id']
                result_dict[result['id']]['album'] = result['album']['name']
                result_list.append(result_dict)
        return_dict = {}
        n = 0
        for result_section in result_list:
            for result in result_section:
                n = n +1
                return_dict[n] = {}
                return_dict[n] = result_section[result]

    return return_dict

def remove_from_playlist(playlist_id,track_list):

    if track_list:

        #print info
        print(str(len(track_list))+" songs will be removed from the playlist")
        print("*******************************")
        track_list_info = track_info_search(track_list) #look up song information to print out
        for track in track_list_info:
            print(track_list_info[track]['artist']+" - "+track_list_info[track]['title']+" - "+track_list_info[track]['album'])
        print()


        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, track_list, snapshot_id=None)
        print("Removal complete")
        print("***********")
    else:
        print("No songs in Removal List!")

def track_search(search_terms):
    #input a list of search terms, each item is one term to search
    #output a list of UUIDs
    #prints out which terms do not find a result
    track_ids = []
    missing_tracks = []
    if isinstance(search_terms, list): #check to see if list
        print(str(len(search_terms))+" search terms given")
        for term in search_terms:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            result = sp.search(term, limit=1, type='track', market='US')
            if result['tracks']['total'] != 0:
                result_title = result['tracks']['items'][0]['name']
                result_artist = result['tracks']['items'][0]['artists'][0]['name']
                result_id = result['tracks']['items'][0]['id']
                track_ids.append(result_id)
            else:
                print(str("TRACK NOT FOUND: " + term))
                missing_tracks.append(term)
        print(str(len(track_ids))+" Tracks found")
        print(str(len(missing_tracks))+" Tracks Not Found")
        return track_ids #returns list of track IDs
    else:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        result = sp.search(search_terms, limit=1, type='track', market='US')
        if result['tracks']['total'] != 0:
            result_title = result['tracks']['items'][0]['name']
            result_artist = result['tracks']['items'][0]['artists'][0]['name']
            result_id = result['tracks']['items'][0]['id']
            #track_ids.append(result_id)
            return result_id
        else:
            print(str("TRACK NOT FOUND: " + search_terms))

def get_user_playlists():
    #input is logged in user
    #output dict of dict. Keys are names, ids are values
    return_dict = {}
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    playlists = sp.current_user_playlists()
    for x in playlists['items']:
        return_dict[x['name']] = x['id']
    return return_dict

def exclusion_terms():
    q_list = ['Q1','Q2','Q3','Q4']
    y_list = list(range(2010,2030))
    plist_list = []
    for y in y_list:
       for q in q_list:
           plist_list.append(str(y)+" "+str(q))
    return plist_list

def user_saved_tracks():
    #returns dictionary of user saved tracks
    #along with add times
    #IDs as keys ad added time as values
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.current_user_saved_tracks(limit=20, offset=0)
    track_dict = {}
    for x in results['items']:
        track_dict[x['track']['id']] = datetime.strptime(x['added_at'],"%Y-%m-%dT%H:%M:%SZ")
    return track_dict

def extended_playlist_search(exclusion_list):
    #input is list of playlist names to exclude from search
    #output is list of UUIDs that are in search_terms playlists
    #add_list = ['COUNTRY', 'STARRED']
    print ("Generating Exclusion List")
    current_playlist_dict = get_user_playlists()
    extended_playlists = []
    for plist in current_playlist_dict:
        if plist in exclusion_list: #checks if above playlists exist in long list of all playlists
            extended_playlists.append(current_playlist_dict[plist]) #adds that playlist to extended_playlist_dict

    previously_added_tracks = []

    for playlist in extended_playlists: #uses playlists in found dictionary
        results = playlist_tracks(playlist) #get results of track ids
        previously_added_tracks = previously_added_tracks + results
    print(str(len(previously_added_tracks))+" Exclusion Songs")
    print("Exclusion Search Complete")
    print()
    return previously_added_tracks

def remove_from_saved(track_list):
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    result = sp.current_user_saved_tracks_delete(track_list)

def add_to_saved(track_list):
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    result = sp.current_user_saved_tracks_add(track_list)

def add_to_playlist(playlist_id,track_list,exclusion_list):
    #input is list of track UUIDs, list of terms to be excluded
    extended_tracks = extended_playlist_search(exclusion_list) #finds tracks from other playlists to compare to
    print("Adding songs to playlist")
    print("************************")
    print()
    add_list = []
    remove_list = []
    for song in track_list: #for the track
        if song in extended_tracks: #if song is in exclusions
            remove_list.append(song) #add to remove list, ie will not be added
        else:
            add_list.append(song) #add song to add list to be added

    if not add_list: #checks to see if list is empty
        print("add_list is Empty, No songs will be added")
        print("*****************************************")
        print()

        print(str(len(remove_list))+" songs are in the exclusions list")
        print("*******************************")
        remove_list_info = track_info_search(remove_list) #look up song information to print out
        for track in remove_list_info:
            print(remove_list_info[track]['artist']+" - "+remove_list_info[track]['title']+" - "+remove_list_info[track]['album'])
        print()
    else:
        print(str(len(add_list))+" songs will be added to the playlist")
        print("*******************************")
        add_list_info = track_info_search(add_list) #look up song information to print out
        for track in add_list_info:
            print(add_list_info[track]['artist']+" - "+add_list_info[track]['title']+" - "+add_list_info[track]['album'])
        print()

        if len(remove_list) != 0:
            print(str(len(remove_list))+" songs are in the exclusions list")
            print("*******************************")
            remove_list_info = track_info_search(remove_list) #look up song information to print out
            for track in remove_list_info:
                print(remove_list_info[track]['artist']+" - "+remove_list_info[track]['title']+" - "+remove_list_info[track]['album'])
            print()
        else:
            print("0 songs are in the exclusions list")
            print("*******************************")
            print()

        if len(add_list) < 100:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            results = sp.user_playlist_add_tracks(username, playlist_id, add_list)
        else:
                list_of_lists = [add_list[i:i+100] for i in range(0, len(add_list), 100)]
                for current_list in list_of_lists:
                    sp = spotipy.Spotify(auth=token)
                    sp.trace = False
                    results = sp.user_playlist_add_tracks(username, playlist_id, current_list) #adds those tracks

def add_to_playlist_return(playlist_id,track_list,exclusion_list):
    #input is list of track UUIDs, list of terms to be excluded
    extended_tracks = extended_playlist_search(exclusion_list) #finds tracks from other playlists to compare to
    print("Adding songs to playlist")
    print("************************")
    print()
    add_list = []
    add_list_info = []
    remove_list = []
    remove_list_info = []

    for song in track_list: #for the track
        if song in extended_tracks: #if song is in exclusions
            remove_list.append(song) #add to remove list, ie will not be added
        else:
            add_list.append(song) #add song to add list to be added

    if not add_list: #checks to see if list is empty
        print("add_list is Empty, No songs will be added")
        print("*****************************************")
        print()

        print(str(len(remove_list))+" songs are in the exclusions list")
        print("*******************************")
        remove_list_info = track_info_search(remove_list) #look up song information to print out
        for track in remove_list_info:
            print(remove_list_info[track]['artist']+" - "+remove_list_info[track]['title']+" - "+remove_list_info[track]['album'])
        print()
    else:
        print(str(len(add_list))+" songs will be added to the playlist")
        print("*******************************")
        add_list_info = track_info_search(add_list) #look up song information to print out
        for track in add_list_info:
            print(add_list_info[track]['artist']+" - "+add_list_info[track]['title']+" - "+add_list_info[track]['album'])
        print()

        if len(remove_list) != 0:
            print(str(len(remove_list))+" songs are in the exclusions list")
            print("*******************************")
            remove_list_info = track_info_search(remove_list) #look up song information to print out
            for track in remove_list_info:
                print(remove_list_info[track]['artist']+" - "+remove_list_info[track]['title']+" - "+remove_list_info[track]['album'])
            print()
        else:
            print("0 songs are in the exclusions list")
            print("*******************************")
            print()

        if len(add_list) < 100:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            results = sp.user_playlist_add_tracks(username, playlist_id, add_list)
        else:
                list_of_lists = [add_list[i:i+100] for i in range(0, len(add_list), 100)]
                for current_list in list_of_lists:
                    sp = spotipy.Spotify(auth=token)
                    sp.trace = False
                    results = sp.user_playlist_add_tracks(username, playlist_id, current_list) #adds those tracks

    return add_list_info,remove_list_info #19/7/22


def get_devices():
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.devices()
    return results

def start_playback(device,uri,shuffle_status):
    #start_playback(device_id=None, context_uri=None, uris=None, offset=None)
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results_2 = sp.shuffle(shuffle_status, device_id=device)
    results = sp.start_playback(device_id=device, context_uri=uri, uris=None, offset=None)
    return results

def top_tracks(): #creates list of 3 playlists

    term_dict = {}
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    ranges = ['short_term', 'medium_term', 'long_term']
    for range in ranges:
        results = sp.current_user_top_tracks(time_range=range, limit=25)
        if range == 'short_term':
            title = "Top Tracks: Short Term"
        if range == 'medium_term':
            title = "Top Tracks: Medium Term"
        if range == 'long_term':
            title = "Top Tracks: Long Term"
        term_dict[title] = []
        for i, item in enumerate(results['items']):
            #w = i + 1
            #term_dict[range][w] = item['id']
            term_dict[title].append(item['id'])
    return term_dict
