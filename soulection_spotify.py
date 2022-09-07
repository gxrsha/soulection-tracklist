import base64, os, io
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import soulection_tracklist as soul
from PIL import Image

load_dotenv()
scope = 'playlist-modify-public, ugc-image-upload'
REDIRECT_URI = 'http://localhost:8080'
uri_list = ['spotify:track:4rdQivUpY3faWSm98gMplo', 'spotify:track:6aQWAtgTQsnNKRTVyG54ST', 'spotify:track:4Y8v3SauBTDS1qbWIKVxcZ', 'spotify:track:0mgFgqJJVNGiaG2oUuSj41', 'spotify:track:6WVVh2gJXQv8tW1Fb5fOa5', 'spotify:track:02mYw61RoS1vXvkD9Q5dpN', 'spotify:track:3U6UHyDRSgWCyvWiBfNFHb', 'spotify:track:6xooozu9X43pLiWwIxphTV', 'spotify:track:2yA2TMbRuV3BpdCqzv4uuX', 'spotify:track:5NaM1Pvh51i5Ja5EMb7D31', 'spotify:track:7BGgytgNrpGXHh00yzOHGx', 'spotify:track:2lv2Asn3LQY1jCQKE6VlNY', 'spotify:track:7E3D5EA6Sv89GNXABU7Xex', 'spotify:track:54huym3Clwn8vsqDeTVETg', 'spotify:track:1c2wTe7doRRk2n1XZe0KAM', 'spotify:track:0J119Oas2ox6JTTHUGZxHN', 'spotify:track:3IT44O4KU7gFFrnLYbLsUG']

def main(client, url):

    # Create our spotify playlist
    playlist_id = create_spotify_playlist(client, url)

    # Add tracks to the playlist
    get_track_uri(client, url, playlist_id)

    # Update image of our newly created playlist
    upload_spotify_playlist_image(client, playlist_id)
    print(f'Successfully created playlist for Episode {soul.get_tracklist_number(url)} - https://open.spotify.com/playlist/{playlist_id}')


def create_spotify_playlist(client, url):
    print("Creating Spotify playlist...")
    playlist_name = f"Soulection Radio Episode #{soul.get_tracklist_number(url)}"
    playlist_description = f"Tracks found in Soulection Radio Episode #{soul.get_tracklist_number(url)} - Listen to the full episode at soundcloud.com/soulection/soulection-radio-show-{soul.get_tracklist_number(url)}"
    playlist = client.user_playlist_create(os.getenv('SPOTIFY_USER_ID'), playlist_name, public=True, collaborative=False, description=playlist_description)
    playlist_id = playlist['id']

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
    client.user_playlist_add_tracks(os.getenv('SPOTIFY_USER_ID'), playlist_id, unique_uri_list, position=None)



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
    tracklist_url = 'https://soulection.com/tracklists/561'
    client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri=REDIRECT_URI, client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET')))
    print(client)
    main(client, tracklist_url)