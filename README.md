# Soulection Tracklist
Creates a Spotify Playlists of tracks from Soulection Radio based on the track list

## Soulection Radio

- Soundcloud - https://soundcloud.com/soulection
- Website - https://soulection.com
- Tracklists - https://soulection.com/tracklists

### To install and run

```bash
pip install -r requirements
python3 soulection_spotify.py
```

`.env` file is required containing two env variables
- `CLIENT_ID` - The ID from the app created on Spotify API
- `CLIENT_SECRET` - Client secret obtained from Spotify API

### Playlists in Spotify
The script ran in the repo will scrape songs off Soulection Tracklist and finds matching songs in Spotify to create a playlist.
Example: https://open.spotify.com/playlist/0kg5HT9f6IodNiOfMTltex

Due to alot of soundcloud artists/tracks not being on Spotify - a way to get around this was using the `add_recommended_songs_to_playlist` method.
This method finds matching songs based on artists and tracks that are within the playlist and adds to the playlist until it hits 40 tracks in total.

### Future Work
- [x] Add more songs to playlist using Spotify's recommendations endpoint
- [ ] Create twitter bot to tweet playlist after its created
