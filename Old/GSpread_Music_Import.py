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
import math
import functions


g_scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', g_scope)
client = gspread.authorize(creds)
spreadsheet = client.open('GMusic Playlist Backup 2017.01.15')

time = datetime.now()

username = credentials.username

scope = 'user-library-read playlist-read-private playlist-modify-public playlist-modify-private user-library-modify'
token = util.prompt_for_user_token(username,scope,client_id=credentials.client_id,client_secret=credentials.client_secret,redirect_uri=credentials.redirect_uri)

f=open("missing_log.txt","w+")
f.close()

def create_search_dictionary(sheet_number):
    dict_1 = {}
    sheet = spreadsheet.get_worksheet(sheet_number)
    cells = sheet.col_values(1)
    print("CURRENT SHEET: "+str(sheet))
    del cells[0]
    return_list = []
    for n,cell in enumerate(cells):
        s = n+1
        if cell == '':
            empty_cell = cell
        else:
            dict_1[s] = {}
            sep1 = ','
            data = cell.split(sep1)
            term_1 = data[0]+" "+data[2].replace('"', "")
            term_2 = term_1.replace('(', '').replace(')', '')
            term_3 = term_2.replace('&', '').replace('feat.', '')
            return_list.append(term_3)
    return return_list #returns dictionary of search terms and sheet name

def create_search_dictionary_special(sheet_number):
    dict_1 = {}
    sheet = spreadsheet.get_worksheet(sheet_number)
    cells = sheet.col_values(1)
    print("CURRENT SHEET: "+str(sheet))
    del cells[0]
    return_list = []
    for n,cell in enumerate(cells):
        s = n+1
        if cell == '':
            empty_cell = cell
        else:
            dict_1[s] = {}
            sep1 = ','
            data = cell.split(sep1)
            term_1 = cell
            term_2 = term_1.replace('(', '').replace(')', '')
            term_3 = term_2.replace('&', '').replace('feat.', '')
            return_list.append(term_3)
    return return_list #returns dictionary of search terms and sheet name

playlist_name = 'STARRED'
exclusion_p1 = [playlist_name]
exclusion_p2 = functions.exclusion_terms()
exclusion_list = exclusion_p1 + exclusion_p2

worksheet_list = spreadsheet.worksheets()
for n,worksheet in enumerate(worksheet_list):
    print(str(n)+" : "+str(worksheet))

while True:
    for n,worksheet in enumerate(worksheet_list):
        print(str(n)+" : "+str(worksheet))
    sheet_number = int(input("What is the playlist number? "))
    search_list = create_search_dictionary(sheet_number) #grabs sheet track search terms and name

    #track_id_list = track_convert(search_list,current_sheet_name) #creats spotify track id list
    track_list = functions.track_search(search_list)
    functions.add_to_playlist(functions.playlist_creation(playlist_name), track_list, exclusion_list)

    #creation_dict = playlist_check_and_creation(track_id_list) #creates dictionary or finds existing
    #add_to_playlist(creation_dict)
    print()
    print()
