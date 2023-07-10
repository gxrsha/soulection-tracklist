import base64, os, io, time
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError
from dotenv import load_dotenv
import soulection_tracklist as soul
from PIL import Image
load_dotenv()
scope = 'playlist-modify-public, ugc-image-upload'
# REDIRECT_URI = 'https://www.google.com'
REDIRECT_URI = 'https://soulection-tracklist.herokuapp.com/oauth'

import json
import os

from spotipy.oauth2 import SpotifyOAuth, SpotifyOauthError

class HerokuCacheHandler(SpotifyOAuth):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_cached_token(self):
        token_info = None

        token_info_str = os.getenv('SPOTIFY_TOKEN_INFO')
        if token_info_str:
            token_info = json.loads(token_info_str)

        if token_info:
            # if scopes don't match, then bail
            if 'scope' not in token_info or not self._is_scope_subset(self.scope, token_info['scope']):
                return None

            if self.is_token_expired(token_info):
                token_info = self.refresh_access_token(token_info['refresh_token'])

        return token_info

    def save_token_info(self, token_info):
        os.environ['SPOTIFY_TOKEN_INFO'] = json.dumps(token_info)


def main(client, url):

    # Create our spotify playlist
    playlist_id = create_spotify_playlist(client, url)

    # Add tracks to the playlist
    get_track_uri(client, url, playlist_id)

    # Update image of our newly created playlist
    upload_spotify_playlist_image(client, playlist_id)

    print(f'Successfully created playlist for Episode {soul.get_tracklist_number(url)} - https://open.spotify.com/playlist/{playlist_id}')
    print_results(url)


def print_results(url):
    print(f"""
         ,_______________________________________,
        /   HHH*                          *HHH   /.
        `---------------------------------------" :
        | +            Playlist {soul.get_tracklist_number(url)}           + | :
        |             .____________.            | :
        |       .++.  |######\  /##|  .++.      | :
        |       +  +  |######/  \##|  +  +      | :
        |       '++'  '------------'  '++'      | :
        |            Spotify Playlist           | :
        |                 gxrsha                | :
        |                                       | :
        |      /'''''''''''''''''''''''''\      I :
        |     /     o       0         o   \     I :
        |+   / O                         O \   +|,'
        `---------------------------------------`


    """)


def create_spotify_playlist(client, url):
    print("Creating Spotify playlist...")
    playlist_name = f"Soulection Radio Episode #{soul.get_tracklist_number(url)}"
    playlist_description = f"Tracks found in Soulection Radio Episode #{soul.get_tracklist_number(url)} - Listen to the full episode at soundcloud.com/soulection/soulection-radio-show-{soul.get_tracklist_number(url)}"
    playlist = client.user_playlist_create(os.getenv('SPOTIFY_USER_ID'), playlist_name, public=True, collaborative=False, description=playlist_description)
    playlist_id = playlist['id']
    print(f"New playlist id: {playlist_id}")

    return playlist_id


def get_track_uri(client, url, playlist_id):
    tracks = soul.get_soulection_tracklist(url)
    print(f"Number of tracks found in Soulection Tracklist: {len(tracks)}")
    list_of_artists = [artists['artist'] for artists in tracks]
    uri_list = []

    for track in tracks:
        sp_track = client.search(q=f"{track['title']} {track['artist']}", limit=1, type=['track'])
        if sp_track['tracks']['items']:
            if sp_track['tracks']['items'][0]['artists'][0]['name'] in list_of_artists:
                # print(f"artist: {sp_track['tracks']['items'][0]['artists'][0]['name']}")
                # print(f"name: {sp_track['tracks']['items'][0]['name']}")
                spotify_uri = sp_track['tracks']['items'][0]['uri']
                uri_list.append(spotify_uri)

    unique_uri_list = list(set(uri_list))

    print(f"Number of tracks found on Spotify: {len(unique_uri_list)}")
    print('Adding songs to playlist..')
    client.user_playlist_add_tracks(os.getenv('SPOTIFY_USER_ID'), playlist_id, unique_uri_list, position=None)

    if len(unique_uri_list) < 40:
        add_recommended_songs_to_playlist(client, playlist_id, unique_uri_list)



def add_recommended_songs_to_playlist(client, playlist_id, uri_of_songs):
    print(f'Adding extra songs..')
    items = client.playlist_items(playlist_id)
    first_five_tracks = items['items'][0:5]

    song_limit = 40 - len(uri_of_songs)
    artist_uri_list = []
    genre_list = []
    recommended_song_uris = []
    
    for track in first_five_tracks:
        artist_uri_list.append(track['track']['artists'][0]['uri'])

    for artist in artist_uri_list:
        artist_info = client.artist(artist)
        if artist_info['genres']:
            genre_list.append(artist_info['genres'][0])
        else:
            continue

   
    # print(f'Our artists: {artist_uri_list}')
    # print(f'Seed genres: {genre_list}')
    # print(f'seed_tracks: {uri_of_songs[0:5]}')
    # print(f'Song limit: {song_limit}')

    songs = client.recommendations(seed_artists=artist_uri_list[0:3], seed_genres=None, seed_tracks=uri_of_songs[0:2], limit=song_limit)

    for song in songs['tracks']:
        recommended_song_uris.append(song['uri'])
    

    client.user_playlist_add_tracks(os.getenv('SPOTIFY_USER_ID'), playlist_id, recommended_song_uris, position=None)
    print('Finished adding additional songs...')
        


def upload_spotify_playlist_image(client, playlist_id):
    print("Uploading image for playlist..")
    base64image = soul.get_tracklist_image(tracklist_url)
    buffer = io.BytesIO()
    imgdata = base64.b64decode(base64image)
    img = Image.open(io.BytesIO(imgdata))
    new_img = img.resize((900, 900))
    new_img.save(buffer, format="jpeg")
    img_b64 = base64.b64encode(buffer.getvalue())
    client.playlist_upload_cover_image(playlist_id, img_b64)



if __name__ == '__main__':

    current_track = 599

    while True:
        latest_track = soul.get_current_tracklist()
        if current_track + 1 == int(latest_track):
            print(f"Found a new track! -- Episode {latest_track}")
            current_track += 1
            tracklist_url = f"https://soulection.com/tracklists/{latest_track}"
            # tracklist_url = f"https://soulection.com/tracklists/600"
            # client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri=REDIRECT_URI, client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET')))
            client = spotipy.Spotify(auth_manager=HerokuCacheHandler(scope=scope, redirect_uri=REDIRECT_URI, client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET')))

            main(client, tracklist_url)
        else:
            print(f"Did not find a new track for Soulection Radio Episode: {current_track + 1}, current track is: {current_track} -- sleeping for 1 hr")
            # Sleep for 1 hour
            time.sleep(5)
