from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = input("В какой год вы хотите вернуться? Напишите в формате YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

#Spotify Аутентификация
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id='ID',
        client_secret='SECRET',
        show_dialog=True,
        cache_path="token.txt"))

user_id = sp.current_user()["id"]

#Поиск песен
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"песня:{song} год:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

#Создаем плейлист
playlist = sp.user_playlist_create(user=user_id, name=f"{date} ТОП 100", public=False)

#Добавляем песни
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
