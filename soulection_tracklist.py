###################################################################
###### July 2022 - Getting latest Soulection Radio Trackliist
###### gxrsha
###################################################################

import requests
import base64
from bs4 import BeautifulSoup

# Returns tracklist songs
def get_soulection_tracklist(url):
    
    response = requests.get(url)

    if response.ok:
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        master_track_list = []

        tracks = soup.find_all('a', {'class': 'track__list-item'})

        for track in tracks:
            track_dictionary = {}
            track_dictionary['title'] = track.find_next('span', {'class': 'flex-grow'}).find_next('span', {'class': 'font-medium order-2 truncate'}).text
            track_dictionary['artist'] = track.find_next('span', {'class': 'flex-grow'}).find_next('span', {'class': 'font-light order-3'}).text
            master_track_list.append(track_dictionary)

        # print(f'{master_track_list}')
        return master_track_list
    else:
        print(f"Tracklist doesn't exist")

# Returns tracklist image as base64
def get_tracklist_image(url):
    track_list_number = url.rsplit('/')[-1]
    image_url = f'https://dy2wnrva.twic.pics/images/episodes/soulection-radio-show-{track_list_number}.jpg'
    return base64.b64encode(requests.get(image_url).content)

# Returns tracklist number
def get_tracklist_number(url):
    return url.rsplit('/')[-1]

# Gets latest track number from site
def get_current_tracklist():
    url = 'https://soulection.com/tracklists'   
    response = requests.get(url)

    if response.ok:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        first_track_href = soup.find('a', {'class': 'dark:hover:bg-gray-800 transition p-4 -mx-4 py-4 flex flex-row items-center'})['href']

        return first_track_href.rsplit('/')[-2]
