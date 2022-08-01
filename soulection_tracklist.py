###################################################################
###### July 2022 - Getting latest Soulection Radio Trackliist
###### gxrsha
###################################################################

import requests
import base64
from bs4 import BeautifulSoup


url = 'https://soulection.com/tracklists/557'
# Returns tracklist songs
def get_soulection_tracklist(url):
    
    response = requests.get(url)

    if response.ok:
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        master_track_list = []

        tracks = soup.find_all('a', {'class': 'track__list-item flex flex-row items-center justify-center p-4 text-lg transition-colors duration-1000 transition dark:hover:bg-gray-800 rounded'})

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


# get_soulection_tracklist(url)