from tkinter import *
import print_dict
import p_s_dict

return_list = {}
playlist_url_list = []
master_button = {}
button_list = ["Song Name", "Artist", "Producer", "Songwriter", "ISRC"]

def var_states(button):
    """
    Will return whether these are clicked as true. (Boolean)
    """
    if button.get() == 1:
        return True
    else:
        return False

def get_all_var_states(var_list, button_list, master_doc):
    """
    Will return all of the Boolean statements for the checkboxes
    """
    for i in range(len(var_list)):
        return_list[button_list[i]] = (var_states(var_list[i]))

    master_button["Master"] = var_states(master_doc)
    return return_list


def define_playlist_url(url_string1, url_string2, url_string3, url_string4):
    playlist_url_list.append(url_string1.get())
    playlist_url_list.append(url_string2.get())
    playlist_url_list.append(url_string3.get())
    playlist_url_list.append(url_string4.get())


def launch_gui():
    master = Tk()
    Label(master, text="Playlist URL").grid(row=0)
    url_input1 = Entry(master)
    url_input1.grid(row = 0, column=1)

    url_input2 = Entry(master)
    url_input2.grid(row = 0, column=2)

    url_input3 = Entry(master)
    url_input3.grid(row = 0, column=3)

    url_input4 = Entry(master)
    url_input4.grid(row = 0, column=4)

    Label(master, text="What do you need from the new songs on this playlist?").grid(row=1, sticky=W)
    song_name = IntVar()
    Checkbutton(master, text="Song Name", variable=song_name).grid(row=2, sticky=W)
    
    artist_name = IntVar()
    Checkbutton(master, text="Artist", variable=artist_name).grid(row=3, sticky=W)
    
    producer_name = IntVar()
    Checkbutton(master, text="Producers", variable=producer_name).grid(row=4, sticky=W)
    
    songwriter_name = IntVar()
    Checkbutton(master, text="Songwriters", variable=songwriter_name).grid(row=5, sticky=W)
    
    isrc_id = IntVar()
    Checkbutton(master, text="ISRC", variable=isrc_id).grid(row=6, sticky=W)

    Label(master, text="CSV Settings").grid(row=7, sticky=W)

    master_doc = IntVar()
    Checkbutton(master, text = "Add to the master doc?", variable = master_doc).grid(row = 8, sticky=W)

    Button(master, text='Submit', command=lambda:[get_all_var_states(var_list, button_list, master_doc), define_playlist_url(url_input1, url_input2, url_input3, url_input4), master.quit()]).grid(row=9, sticky=W, pady=4)

    # Label(master, text="Click these if you'd like to create a producer/songwriter dictionary.").grid(row = 10, sticky=W)

    # Button(master, text="Producers", command=print_dict.get_type_and_sort('Producers')).grid(row=11, sticky=W, pady=4)

    # Button(master, text="Songwriters", command=print_dict.get_type_and_sort('Songwriters')).grid(row=12, sticky=W, pady=4)

    var_list = [song_name, artist_name, producer_name, songwriter_name, isrc_id]

    mainloop()

launch_gui()

# print("This is the playlist_url: " + playlist_url[0])



