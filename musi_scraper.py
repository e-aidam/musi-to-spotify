# scrapes playlist name, video titles, and video artists from musi playlist url

# importing modules for scraping dynamic content from website
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 

# input musi url
url = input('Enter Musi playlist url')
""" check for correct format, 
https://feelthemusi.com/playlist/######, 
5 lettter/number identifier"""
 
# instantiate options 
options = webdriver.ChromeOptions() 
 
# run browser in headless mode 
options.headless = True 
 
# start driver 
driver = webdriver.Chrome(service=ChromeService( 
    ChromeDriverManager().install()), options=options) 
 
# load website 
driver.get(url) 

try:
    # wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "video_title")))


    # find all elements with class "video_title" and "video_artist" and id "playist_header_title"
    video_titles = driver.find_elements(By.CLASS_NAME, 'video_title')
    video_artists = driver.find_elements(By.CLASS_NAME, 'video_artist')
    playlist_title = driver.find_element(By.ID, 'playlist_header_title')
        
    """
    Also create if statement to remove '- Topic' from video_artist
    for video_artist in video
    if video_artist contains '- Topic':
        video_artist = video_artist without Topic tag
        
    Remove Audio, Lyrics, Official Audio, Official Video, and Vizualizer from video_title, often in () or []

        Try to add ft./feat./feautring, to video_artist ()

    Add if statement to get song info from title alone when '-' is present (check for long hash as well)
    if video_title contains '-':
        1st half = video_artist
        2nd half = video_title
        
    for video_title in video_titles:
        if video_title
            
 
    """
    
    # create variable for the playlist name
    playlist_name = playlist_title.text
    
    # create a list to store the video information
    source_playlist = []
    
    
            
    # extract text from each element and store it in a list of dictionaries
    for title, artist in zip(video_titles, video_artists):
        source_playlist.append({
                "track_name": title.text,
                "artist": artist.text
            })
    
   
            
finally:
    # close the WebDriver
    driver.quit()

print(source_playlist)
"""
# save playlist as a csv file

# importing modules for csv packaging
import pandas as pd
from pandas import DataFrame
import re

# Convert source_playlist to a DataFrame
df = pd.DataFrame(source_playlist)


# function to Pythonify the playlist name
def pythonify_playlist_name(playlist_name):
    # remove special characters and replace spaces with underscores
    pythonified_name = re.sub(r'[^a-zA-Z0-9\s]', '', playlist_name)
    pythonified_name = pythonified_name.replace(' ', '_')
    # convert to lowercase
    pythonified_name = pythonified_name.lower()
    return pythonified_name

# pythonify the playlist name
pythonified_playlist_name = pythonify_playlist_name(playlist_name)

# define the CSV file name based on the pythonified playlist name
csv_filename = f"{pythonified_playlist_name}data.csv"

# write DataFrame to CSV
df.to_csv(csv_filename, index=False)

print(f"CSV file '{csv_filename}' has been created successfully.")
"""