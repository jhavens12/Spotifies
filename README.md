# Spotifies
Experimenting with the Spotify API

Requires https://github.com/plamere/spotipy
pip3 install git+https://github.com/plamere/spotipy.git --upgrade

Had trouble figuring out how to set these variables, apparently you just run these from the terminal individually

export SPOTIPY_CLIENT_ID='your-spotify-client-id'

export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'

export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

Set up credentials.py file which has spotify api access. While available through the OS using above commands, i thought this more comfortable

# Saved_Tracks.py

Script will take all of your saved tracks from your library and place them in new playlists appropriate to when you "saved" the track based on year and quarter.
It also searches all other playlists matching this naming scheme ex 2018 Q1 or 2017 Q4
Script then removes your saved tracks from being saved

# Duplicate_Track_Search.py

Script will give you a playlist picker where you can choose any of your playlists
Script will then go through and find any potential duplicate songs based on track and artist name
You can then type in any number separated by comma to remove those songs from the playlist

# functions.py

This holds most of the functions that I use

# Duplicate_Playlist.py

This is what the project started as. It takes playlist links and creates a duplicate for you so you can archive shared playlists that you like.
This needs to be updated to use the functions.py file instead of its own functions.

# Current_Top_Tracks.py

Takes your short term, medium term and long term playlists as recorded by spotify and creates playlists for each, if run a second time it will update these playlists by removing tracks that have fallen off and add new tracks.
