import functions
from pprint import pprint
import datetime
import credentials

######
playback_device = credentials.swa2178
######

playlist_name = functions.get_my_current_quarter_playlist() #find current quarter playlist

playlist_id = functions.get_playlist_id(playlist_name) #get that playlist's id

quarter_playlist = "spotify:user:"+credentials.username+":playlist:"+playlist_id #concatinate to make uri

shuffle = True #enable shuffle
functions.start_playback(playback_device,quarter_playlist,shuffle) #start playback
