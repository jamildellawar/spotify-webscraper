import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import csv
from csv import DictWriter
from csv import reader
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="d53aef5f070646cdb962ab13be1eebbc",
                                                           client_secret="cafa8a013afb4bf3afcd149b6569ee6e"))


# Helper Functions

def get_playlist_id(playlist_url):
    """
    Asks for embed code here and returns the playlist code as a string to be used later.

    Returns:
    ID - The Playlist ID (str)
    """

    ID = ""
    
    if playlist_url[0] == "<":
        ID = playlist_url.split('"')[1].split('/')[-1]
    elif playlist_url[0:5] == "https":
        ID = playlist_url.split('/')[4].split('?')[0]
    return ID

def quotes(word):
    """
    Takes in a word and put's quotes around it.
    """
    return '"' + word + '"'

def get_bunches_and_total(id):
    """
    With the playlist ID, it will return an array of all tracks (in bunches of 50)
    and the total amount of tracks.
    """
    temp = []
    # Add's the first bunch up to 100 songs
    temp.append(sp.playlist_tracks(id, fields='items.track, total'))
    # Get the total amount of songs in the playlist
    total_number_of_tracks = temp[0]['total']
    temp_total_amount = temp[0]['total']
    offset_num = 100
    # If there is still more 
    while temp_total_amount > 100:
        temp.append(sp.playlist_tracks(id, fields='items.track, total', offset=offset_num))
        temp_total_amount -= 100
        offset_num += 100
    return (temp, total_number_of_tracks)

def add_song_names(bunches):
    """
    Within the bunches given, we'll scan for all the song names
    and return a list of the song names
    """
    temp = []
    # For however many bunches...
    for i in range(len(bunches)):
        # Add each song in this bunch
        for j in range(len(bunches[i]['items'])):
            try:
                temp.append(bunches[i]['items'][j]['track']['name'])
            except TypeError:
                print("Blank Item")
    return temp

def add_artists(bunches):
    """
    Within the bunches given, we'll scan for all the artist names
    and return a list of the artist names
    """
    temp = []
    # For each bunches...
    for i in range(len(bunches)):
        # for each song in the bunch
        for j in range(len(bunches[i]['items'])):
            # for each artist in the song create a new list for that song
            temp_artists = []
            try:
                for x in range(len(bunches[i]['items'][j]['track']['artists'])):
                    temp_artists.append(bunches[i]['items'][j]['track']['artists'][x]['name'])
                # and append that list into the final list to be returned
                temp.append(temp_artists)
            except TypeError:
                print("Blank Item")
    return temp

def add_isrc(bunches):
    """
    Within the bunches given, we'll scan for all the artist names
    and return a list of the artist names
    """
    temp = []
    # For however many bunches...
    for i in range(len(bunches)):
        # Add each song in this bunch
        for j in range(len(bunches[i]['items'])):
            # Get the ISRC
            try:
                temp.append(bunches[i]['items'][j]['track']['external_ids']['isrc'])
            except TypeError:
                print("Blank Item")
    return temp

def combine_song_info_list(song_name_list, artist_name_list, isrc_list, songwriters_list = None, producers_list=None):
    """
    Parameters:
    song_name_list - a list of all song names
    artist_name_list - a list of all artist names
    isrc_list - a list of all ISRC IDs
    songwriters_list - a list of all songwriters (can be NoneType)
    producers_list - a list of all producers (can be NoneType)

    Returns:
    ans - a list [{'song': song name, 'artist': artist name, 'isrc': isrc id, 'songwriter': songwriters list, 'producer': producer list}, ...]
    """
    ans = []
    for index in range(len(song_name_list)):
        temp = {}
        if song_name_list != None:
            temp['Song Name'] = song_name_list[index]
        if artist_name_list != None:
            temp['Artist'] = artist_name_list[index]
        if isrc_list != None:
            temp['ISRC'] = isrc_list[index]
        if songwriters_list != None:
            print(songwriters_list)
            print(producers_list)
            temp['Songwriter'] = songwriters_list[index]
        if producers_list != None:
            temp['Producer'] = producers_list[index]
        ans.append(temp)
    return ans

def combine_song_info_dict(song_name_list, artist_name_list, isrc_list, songwriters_list, producers_list):
    """
    Parameters:
    song_name_list - a list of all song names
    artist_name_list - a list of all artist names
    isrc_list - a list of all ISRC IDs
    songwriters_list - a list of all songwriters (can be NoneType)
    producers_list - a list of all producers (can be NoneType)

    Returns:
    ans - a dict [{irsc id: {'song': song name, 'artist': artist name, 'isrc': isrc id, 'songwriter': songwriters, producer': producers}, ...}]
    """
    ans = {}
    for index in range(len(song_name_list)):
        temp = {}
        if song_name_list != None:
            temp['Song Name'] = song_name_list[index]
        if artist_name_list != None:
            temp['Artist'] = artist_name_list[index]
        if isrc_list != None:
            temp['ISRC'] = isrc_list[index]
        if songwriters_list != None:
            temp['Songwriter'] = songwriters_list[index]
        if producers_list != None:
            temp['Producer'] = producers_list[index]
        
        # Dictionary based on ISRC
        ans[isrc_list[index]] = temp
    return ans

def artist_to_string(artist_list):
    """
    Returns the artst names (in a list) as a clean string
    """
    artist_string = artist_list[0]
    counter = 1
    while len(artist_list) > counter:
        artist_string += ", " + artist_list[counter]
        counter += 1
    
    return artist_string


def append_dict_in_csv(file_name, song_name, artist_name, producer, songwriter, isrc):
    """
    Add dictionary entries to the file
    """
    # Open file in append mode
    with open(file_name, 'a') as f_object:
        field_names = ['Song Name', 'Artist Name', 'Producer', 'Songwriter', 'ISRC']
        # Pass the file object and a list 
        # of column names to DictWriter()
        # You will get a object of DictWriter
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
    
        # Pass the dictionary as an argument to the Writerow()
        dict = {'Song Name': song_name, 'Artist Name': artist_name, 'Producer': producer, 'Songwriter' : songwriter, 'ISRC': isrc}
        
        dictwriter_object.writerow(dict)


def print_names(name_list):
    name_string = ""
    temp = 0

    if type(name_list) != list:
        return name_list

    for name in name_list:
        if temp == 0:
            name_string += name
            temp += 1
        else:
            name_string += ", " + name

    return name_string

# def append_songs_covered(button_list, ):

