# Soulection Tracklist
Creates a Spotify Playlists of tracks from Soulection Radio based on the track list

## Soulection Radio

- Soundcloud - https://soundcloud.com/soulection
- Website - https://soulection.com
- Tracklists - https://soulection.com/tracklists

### To install and run

```bash
pip install -r requirements
```

`.env` file is required containing two env variables
- `CLIENT_ID` - The ID from the app created on Spotify API
- `CLIENT_SECRET` - Client secret obtained from Spotify API

### Playlists in Spotify
The script ran in the repo will scrape songs off Soulection Tracklist and finds matching songs in Spotify to create a playlist.
Example: https://open.spotify.com/playlist/4OoqtelbOxjhNJ2dvBS0DE?si=d1eabf0dbfa542ad

### Future Work
- [ ] Add more songs to playlist using Spotify's recommendations endpoint
- [ ] Create twitter bot to tweet playlist after its created
