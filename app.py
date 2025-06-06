from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

year_to_listen = input("What year hot hits would you like to listen too? (YYY-MM-DD): ")
URL = f"https:/website/{year_to_listen}/" #web scrapes title songs from a specific year

response = requests.get(URL)
hot_hits_page = response.text

soup = BeautifulSoup(hot_hits_page, "html.parser")
song_title = soup.select("html tags")
song_titles = [song.getText().strip() for song in song_title]
#print(song_titles)

CLIENT_ID = "CLIENT_ID from Spotify"
CLIENT_SECRET = "CLIENT_SECRET from Spotify"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="e.g. https://webpage.com", # to access the token
                                               show_dialog=False,
                                               cache_path="where to recieve access token e.g. text file",
                                               scope="playlist-modify-private", # creates public or private playlist
                                               username="username"))
user_id = sp.current_user()["id"]
#print(results)

song_uri = []
year = year_to_listen.split("-")[0]

for song in song_titles:
    track = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(track)
    try:
        uri = track["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} not available on Spotify. Skipped.")

create_playlist = sp.user_playlist_create(user=user_id,
                                          name=f"{year_to_listen} playlist name",
                                          public=False,
                                          collaborative=False,
                                          description="Playlist description")
#print(create_playlist)

sp.playlist_add_items(playlist_id=create_playlist["id"], items=song_uri)
