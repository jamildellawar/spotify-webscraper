import playlisting as p
import csv
from datetime import datetime

def get_date():
    now = datetime.now()
    return now.strftime("%m-%d-%Y")

def make_one_new_csv(playlist_name, button_list, return_list, song_info_list, song_info_dict, isrc_ids):
    with open(playlist_name + f' on {get_date()}.csv', 'w', newline='') as file:
        fieldnames = []
        temp_song_info = {}
        for item in button_list:
            if return_list[item]:
                fieldnames.append(item)
        for isrc in isrc_ids:
            for item in button_list:
                if return_list[item]:
                    temp_song_info[item] = song_info_dict[isrc][item]
            
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for song in song_info_list:
            write_row_dict = {}
            for item in button_list:
                if return_list[item]:
                    write_row_dict[item] = p.print_names(song[item])
            writer.writerow(write_row_dict)

def make_new_master_playlist_csv(playlist_name, button_list, return_list, song_info_list, song_info_dict, isrc_ids):    
    
    # Create New Master Doc for this Playlist
    with open(f'All Songs In {playlist_name}.csv', 'w', newline='') as file:
        # Use button_list as the fieldname for the master doc
        writer = csv.DictWriter(file, fieldnames=button_list)
        writer.writeheader()

        for song in song_info_list:
            write_row_dict = {}
            for item in button_list:
                write_row_dict[item] = p.print_names(song[item])
            writer.writerow(write_row_dict)
    
    # Show what the user wants right now in this new CSV File
    with open(f'New Songs In {playlist_name} on {get_date()}.csv', 'w', newline='') as file:
        # Get fieldnames (in case it is different)
        fieldnames = []
        for item in button_list:
            if return_list[item]:
                fieldnames.append(item)

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for song in song_info_list:
            write_row_dict = {}
            for item in button_list:
                if return_list[item]:
                    write_row_dict[item] = p.print_names(song[item])
            writer.writerow(write_row_dict)

def update_master_playlist_csv(playlist_name, button_list, return_list, song_info_list, song_info_dict, isrc_ids):
    # Get a list of all ISRC values we've already checked
    to_check = []
    temp_isrc = []
    # open file in read mode
    with open(f'All Songs In {playlist_name}.csv', mode='r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.DictReader(read_obj)

        for row in csv_reader:
            temp_isrc.append(row['ISRC'])
    for isrc in isrc_ids:
        # Check if the songs from the playlist are already in this CSV File 
        if isrc not in temp_isrc:
            temp_song_info = {}
            for item in button_list:
                temp_song_info[item] = song_info_dict[isrc][item]

            p.append_dict_in_csv(f'All Songs In {playlist_name}.csv', temp_song_info['Song Name'], p.artist_to_string(temp_song_info['Artist']), p.artist_to_string(temp_song_info['Producer']), p.artist_to_string(temp_song_info['Songwriter']), temp_song_info['ISRC'])  
            to_check.append(temp_song_info)
            # print(to_check)

    with open(f'New Songs In {playlist_name} on {get_date()}.csv', 'w', newline='') as file:
        # Get fieldnames
        fieldnames = []
        for item in button_list:
            if return_list[item]:
                fieldnames.append(item)

        # If there are new songs to input...
        if len(to_check) != 0:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            # For each song
            for song in to_check:
                # Add the items to the dictionary and writer the row
                row_to_write = {}
                for item in fieldnames:
                    row_to_write[item] = p.print_names(song[item])
                writer.writerow(row_to_write)

        else:
            fieldnames = ['Song Name', 'Artist Name', 'ISRC']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Song Name': "No", 'Artist Name': "New", 'ISRC': "Songs"})
            
def p_s_dict_print(specific_type, person_to_songs_dict):
    capatalized = specific_type[0].capitalize() + specific_type[1:]
    with open('All ' + capatalized + f'.csv', 'w', newline='') as file:
        fieldnames = [capatalized, 'Songs', '# Of Songs']
            
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        names = person_to_songs_dict[specific_type]
        songs = person_to_songs_dict['Songs']

        person_counter = 0
        for name in names:
            row_to_write = {}
            row_to_write[capatalized] = name
            row_to_write['Songs'] = songs[person_counter]
            row_to_write['# Of Songs'] = len(songs[person_counter])
            writer.writerow(row_to_write)
            person_counter += 1
