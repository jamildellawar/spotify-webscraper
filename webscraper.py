# Format of the webplayer link (for playlist):
# https://open.spotify.com/playlist/{PLAYLIST_ID}
import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from gui import master_button
import p_s_dict

# from WebScraperForAllMusic import parserForInformation

def getSongwritersAndProducers(playlist_id, total_amount_of_tracks, song_names = None, ISRC_IDs = None):
    """
    
    """
    # Open webdriver
    browser = webdriver.Chrome(ChromeDriverManager().install())

    # Initialize what we'll return
    songwriters = []
    producers = []


    # Go to the Spotify Playlist link in the Web Player
    playlist_link = "https://open.spotify.com/playlist/" + playlist_id
    browser.get(playlist_link)
    # Maximize the window
    browser.maximize_window()
    # Give it time just in case
    time.sleep(3)
    print("This is the total amount of songs: " + str(total_amount_of_tracks))
    time_counter = 0
    # Get a list of all Songwriters and Producers by
    # Going through each song...
    try:
        for song in range(1, total_amount_of_tracks+1):   
            if time_counter % 15 == 0:
                time.sleep(1) 
            if time_counter % 49 == 0:
                time.sleep(1)
            time_counter += 1
            # Click more options for the song
            print(song)
            try: 
                song_section_menu_button = browser.find_element_by_xpath(f"//div[@role='grid']/div[2]/div[2]/div[@aria-rowindex='{song+1}']/div/div[5]/button[2]")
            except selenium.common.exceptions.NoSuchElementException:
                print("couldn't find button")
            try:
                song_section_menu_button.click()
            except selenium.common.exceptions.NoSuchElementException:
                print("couldn't click the button")
            # Click See Credits
            try:
                song_credits_button = browser.find_element_by_xpath("/html/body/div[15]/div/ul/li[5]/button")
            except selenium.common.exceptions.NoSuchElementException:
                print("couldn't find the button for credits")
            try:
                song_credits_button.click()
            except selenium.common.exceptions.NoSuchElementException:
                print("couldn't click the credits button")
            # Wait a bit
            time.sleep(1)

            songwriter_done = False
            producer_done = False
            # Inititalize this one song's songwriters and producers list
            current_songwriters = []
            current_producers = []
            print("This is song number " + str(song))
            # Get the songwriters
            try:
                a_songwriter_counter = 1
                span_songwriter_counter = 1
                while not songwriter_done:
                    try:
                        songwriter_credits = browser.find_element_by_xpath(f"//div[@class = 'GenericModal ']/div/div[2]/div/div[2]/a[{str(a_songwriter_counter)}]")
                        a_songwriter_counter += 1
                    except selenium.common.exceptions.NoSuchElementException:
                        songwriter_credits = browser.find_element_by_xpath(f"//div[@class = 'GenericModal ']/div/div[2]/div/div[2]/span[{str(span_songwriter_counter)}]")
                        span_songwriter_counter += 1
                    # Add to the master doc
                    if master_button["Master"]:
                        p_s_dict.save_into_master_doc('songwriter', songwriter_credits.text, song_names[song-1], ISRC_IDs[song-1])
                    current_songwriters.append(songwriter_credits.text)
            except selenium.common.exceptions.NoSuchElementException:
                songwriter_done = True

            # Get the producers
            try:
                a_producer_counter = 1
                span_producer_counter = 1
                while not producer_done:
                    try:
                        producer_credits = browser.find_element_by_xpath(f"//div[@class = 'GenericModal ']/div/div[2]/div/div[3]/a[{str(a_producer_counter)}]")
                        a_producer_counter += 1
                    except selenium.common.exceptions.NoSuchElementException:
                        producer_credits = browser.find_element_by_xpath(f"//div[@class = 'GenericModal ']/div/div[2]/div/div[3]/span[{str(span_producer_counter)}]")
                        span_producer_counter += 1
                    # Add to the master doc
                    if master_button["Master"]:
                        p_s_dict.save_into_master_doc('producer', producer_credits.text, song_names[song-1], ISRC_IDs[song-1])
                    current_producers.append(producer_credits.text)
            except selenium.common.exceptions.NoSuchElementException:
                producer_done = True

            
            if len(current_songwriters) == 0:
                current_songwriters.append("-")
            if len(current_producers) == 0:
                current_producers.append("-")
            
            print(song)
            print(current_producers)
            print(current_songwriters)

            songwriters.append(current_songwriters)
            producers.append(current_producers)
            close_button = browser.find_element_by_xpath(f"//div[@class = 'GenericModal ']/div/div[1]/button")
            close_button.click()
    except selenium.common.exceptions.NoSuchElementException:
        print("Done")
    return (songwriters, producers)

# print(getSongwritersAndProducers('37i9dQZF1DWUa8ZRTfalHk', 85))
