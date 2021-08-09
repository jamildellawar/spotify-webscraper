import csv_writer
import p_s_dict


def get_type_and_sort(specific_type, published = None):
    
    specific_doc = p_s_dict.get_master_doc(specific_type)

    person_to_songs = {specific_type: [], 'Songs': []}
    for name in specific_doc.keys():
        person_credits = specific_doc[name]
        if published == {False, True}:
            if published:
                if person_credits[specific_type]:
                    songs = person_credits['Songs']['Name']
            elif not published:
                if not person_credits[specific_type]:
                    songs = person_credits['Songs']['Name']
        else:
            songs = person_credits['Songs']['Name']

        person_to_songs[specific_type].append(name)
        person_to_songs['Songs'].append(songs)


    csv_writer.p_s_dict_print(specific_type, person_to_songs)
    
