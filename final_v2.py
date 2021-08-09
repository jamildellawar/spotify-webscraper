import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from gui import return_list
from gui import playlist_url_list
from gui import button_list
from gui import master_button

import csv_writer

import time

import playlisting as p
import webscraper as ws

from p_s_dict import *

import print_dict

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="INSERT YOUR CLIENT ID",
                                                           client_secret="INSERT YOUR CLIENT SECRET"))



# This is the estimated max we can get 
# with the webscrapper because of the way 
# the website loads
playlist_max = 1000

#Launch the GUI

def do_it(playlist_url):
    # Get the Playlist ID
    playlist_id = p.get_playlist_id(playlist_url)

    # Get the Playlist Name
    playlist_name = sp.playlist(playlist_id)['name']

    # Get all the playlist track info (in bunches) and the 
    # total amount of tracks in this playlist
    playlist_tracks_bunches = p.get_bunches_and_total(playlist_id)[0]
    total_amount_of_tracks = p.get_bunches_and_total(playlist_id)[1]

    # Get all song names from the tracks in bunches
    song_names = p.add_song_names(playlist_tracks_bunches)

    # Get all artist names from the tracks in bunches
    artist_names = p.add_artists(playlist_tracks_bunches)

    # Get all ISRC IDs rom the tracks in bunches
    isrc_ids = p.add_isrc(playlist_tracks_bunches)

    # Criteria to use the webscraper:
    # 1. The person has to be asking for the Producer or Songwriters OR want to update the master sheet
    # 2. The total amount of tracks has to be less than the estimated max for the webscraper to work (56)
    if (master_button["Master"] or return_list["Producer"] or return_list["Songwriter"]) and total_amount_of_tracks < playlist_max:
        songwriters_and_producers = ws.getSongwritersAndProducers(playlist_id, total_amount_of_tracks, song_names, isrc_ids)
        songwriters = songwriters_and_producers[0]
        producers = songwriters_and_producers[1]

    # We need to check if Criteria #2 fails...
    elif total_amount_of_tracks >= playlist_max and master_button["Master"]:
        print("Please use a playlist with less than 56 tracks to add to the master")
        songwriters = None
        producers = None
        return_list['Producer'] = False
        return_list['Songwriter'] = False
        master_button["Master"] = False

    # Otherwise, it just isn't needed
    else:
        songwriters = None
        producers = None
        return_list['Producer'] = False
        return_list['Songwriter'] = False

    # Get a list of the song infos
    song_info_list = p.combine_song_info_list(song_names, artist_names, isrc_ids, songwriters, producers)

    # Get a dict of the song infos with the keys being ISRC IDs
    song_info_dict = p.combine_song_info_dict(song_names, artist_names, isrc_ids, songwriters, producers)


    # Prints the songs
    print("Songs from the playlist " + playlist_name)
    for song in song_info_list:
        # Print in the console to see if 
        print(p.quotes(song['Song Name']) + ' by ' + p.artist_to_string(song['Artist']))

    if master_button["Master"]:
        # Check if there already a file with this playlist name
        try:
            csv_writer.update_master_playlist_csv(playlist_name, button_list, return_list, song_info_list, song_info_dict, isrc_ids)
        
        # If there isn't create this file...
        except FileNotFoundError:
            # Create a new master doc for this playlist and show 
            # what the user wants right now in the New Songs CSV File
            csv_writer.make_new_master_playlist_csv(playlist_name, button_list, return_list, song_info_list, song_info_dict, isrc_ids)
    else:
        csv_writer.make_one_new_csv(playlist_name, button_list, return_list, song_info_list, song_info_dict, isrc_ids)

    print_dict.get_type_and_sort('producers')
    print_dict.get_type_and_sort('songwriters')

counter = 0
for url in playlist_url_list:
    print(counter)
    counter += 1
    if len(url) > 0:
        do_it(url)
