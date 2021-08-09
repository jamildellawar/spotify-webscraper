import json

def get_master_doc(type_of_dict):
    """
    Returns the json package as a dictionary
    """
    with open('master_dict_' + type_of_dict + '.json', 'r') as f:
        datastore = json.load(f)
        return datastore


def save_into_master_doc(type_of_person, name, song_name, isrc, published = False, artist = False):
    """
    
    """
    producer_doc = get_master_doc("producers")
    songwriter_doc = get_master_doc("songwriters")

    if type_of_person == 'producer':
        if name not in producer_doc.keys():
            producer_doc[name] = {'Songs': {'Name': [song_name], 'ISRC': [isrc]}, 'Published': published, 'Artist': artist}
        else:
            if isrc not in producer_doc[name]['Songs']['ISRC']:        
                producer_doc[name]['Songs']['Name'].append(song_name) 
                producer_doc[name]['Songs']['ISRC'].append(isrc)
    elif type_of_person == 'songwriter':
        if name not in songwriter_doc.keys():
            songwriter_doc[name] = {'Songs': {'Name': [song_name], 'ISRC': [isrc]}, 'Published': published, 'Artist': artist}
        else:
            if isrc not in songwriter_doc[name]['Songs']['ISRC']:
                songwriter_doc[name]['Songs']['Name'].append(song_name) 
                songwriter_doc[name]['Songs']['ISRC'].append(isrc)

    save_dictionary(producer_doc, songwriter_doc)


def save_dictionary(producer_doc = None, songwriter_doc = None):
    """
    """
    if producer_doc != None:
        master_doc_file = open("master_dict_producers.json", "w")
        json.dump(producer_doc, master_doc_file)
        master_doc_file.close()

    if songwriter_doc != None:
        master_doc_file = open("master_dict_songwriters.json", "w")
        json.dump(songwriter_doc, master_doc_file)
        master_doc_file.close()

def update_published_or_artist_type(name, published_or_artist, are_they, specific_type = None):
    """
    """
    producers = get_master_doc("producers")
    songwriters = get_master_doc("songwriters")

    if specific_type == None:
        if name in producers.keys() or name in songwriters.keys():
            if name in producers.keys():
                producers[name][published_or_artist] = are_they
            if name in songwriters.keys():
                songwriters[name][published_or_artist] = are_they
        # else:
        #     print("Artist isn't in the master doc")
    elif specific_type in {'producers', 'songwriters'}:
        specific_credit_type = get_master_doc(specific_type)
        if name in specific_credit_type.keys():
            specific_credit_type[name][published_or_artist] = are_they
    #     else:
    #         print("This person is not a " + specific_type)
    # else: 
    #     print("Didn't work")
    
    save_dictionary(producers, songwriters)


def get_amount_of_songs(name):
    """
    """
    producers = get_master_doc("producers")
    songwriters = get_master_doc("songwriters")
    producer_credits = 0
    songwriter_credits = 0

    if name in producers.keys():
        producer_credits = len(producers[name]['Songs'])
    if name in songwriters.keys():
        songwriter_credits = len(songwriters[name]['Songs'])
    
    print(name + " has producing credits on " + str(producer_credits) + " song(s) and songwriting credits on " + str(songwriter_credits) + " song(s).")



