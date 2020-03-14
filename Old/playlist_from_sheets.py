from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
import credentials
from datetime import datetime
from pprint import pprint
import functions
import pygsheets

gc = pygsheets.authorize()

# Open spreadsheet and then workseet
sh = gc.open('The Buzz Top 99 of YEAR')
wks = sh.worksheet_by_title("DECADE")



username = credentials.username

scope = 'user-library-read playlist-read-private playlist-modify-public playlist-modify-private user-library-modify'
token = util.prompt_for_user_token(username,scope,client_id=credentials.client_id,client_secret=credentials.client_secret,redirect_uri=credentials.redirect_uri)

f=open("missing_log.txt","w+")
f.close()

def search_sheet():
    results = wks.range('A1:B99')

    export_dict = {}
    n = 0
    for line in results:
        n = n+1
        export_dict[n] = {}
        export_dict[n][line[0].value] = line[1].value

    export_list = []
    for line in results:
        export_list.append(line[0].value+" "+line[1].value)
    #pprint(export_dict)
    return export_list

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



search_list = search_sheet()
#exclusion_p1 = [playlist_name]
#exclusion_p2 = functions.exclusion_terms()
#exclusion_list = exclusion_p1 + exclusion_p2

# worksheet_list = spreadsheet.worksheets()
# for n,worksheet in enumerate(worksheet_list):
#     print(str(n)+" : "+str(worksheet))


exclusion_list = []
track_list = functions.track_search(search_list)
functions.add_to_playlist(functions.playlist_creation("Top 99 of Decade"), track_list, exclusion_list)

#creation_dict = playlist_check_and_creation(track_id_list) #creates dictionary or finds existing
#add_to_playlist(creation_dict)
