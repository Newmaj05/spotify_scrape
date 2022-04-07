# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 20:57:35 2022

@author: andrew
"""
import requests
from bs4 import BeautifulSoup
import unicodedata
import re
import spotipy
import cred
from spotipy.oauth2 import SpotifyOAuth

url = "https://ultimateclassicrock.com/progressive-rock-songs/"
url2 = "https://www.popmatters.com/141547-best-25-rock-songs-of-all-time-2496025727.html"
page = requests.get(url)
page2 = requests.get(url2)

soup = BeautifulSoup(page.content, "html.parser",from_encoding='ascii')
soup2 = BeautifulSoup(page2.content, "html.parser",from_encoding='ascii')

pagetext = requests.get(url).text
page2text = requests.get(url2).text

souptext = BeautifulSoup(page.content, "lxml")
souptext2 = BeautifulSoup(page2.content, "lxml")

print(souptext.prettify())

raw_text = souptext.find_all("strong")
raw_results = soup.find_all("strong")

#bs.find_all('table', attrs={'border': '1' ,'style':'background-color:White;font-size:10pt;border-collapse:collapse;'})

headers = []
for s in raw_results:
    s_new = s.get_text()
    s_new = unicodedata.normalize("NFKD",s_new)
    headers.append(s_new)

song_list = []
for song in headers:
    new_song = song.lstrip('0123456789.- ')
    artist = new_song.rpartition('-')[0]
    song_match = re.search(r"""(?<=\").+?(?=\")""",new_song)
    song_match = song_match.group()
    song_list.append([song_match,artist])

redirect_uri = 'http://localhost:8889/callback/'
#specify wide range of scopes
scope = "user-library-read playlist-read-collaborative playlist-read-private playlist-modify-public"
#configure authorization using spotipy library, uses values from the cred.py file
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id,
                                               client_secret=cred.client_secret,
                                               redirect_uri=redirect_uri, scope=scope))
    
def spotify_song_check(songs):
    song_details = []
    track_ids_list = []
    for song in songs:
        song_name = str(song[0])
        artist_name = str(song[1])
        searchResults = sp.search(q="artist:" + artist_name + " track:" + song_name, type="track")
        
        for x in searchResults['tracks']['items'][:1]:
            name = x['name']
            artist = x['artists'][0]['name']
            artist_uri = x['artists'][0]['uri']
            album = x['album']['artists'][0]['name']
            song_id = x['id']
            uri = x['uri']
            song_details.append([name, artist,artist_uri, album,song_id,uri])
            track_ids_list.append(song_id)

    return song_details, track_ids_list

def playlist_names_ids(user):
    user_playlists = sp.user_playlists(user)
    playlist_details = {}
    playlist_names = []
    for i in user_playlists['items']:
        name = i['name']
        ids = i['id']
        playlist_names.append(name)
        playlist_details.update({name:ids})
    return playlist_details, playlist_names

def create_playlist(playlist_name,user):
    #user_playlists = sp.user_playlists(user)
    playlist_details = playlist_names_ids(user)
    if playlist_name in playlist_details[1]:
        print("{} is already created".format(playlist_name))
    else:
        print("{} is not created, creating now!".format(playlist_name))
        sp.user_playlist_create(user, name=spotify_pl_name)

def find_playlist_id(playlist_list,playlist_name):
    if playlist_name in playlist_list[0].keys():
        playlist_id = playlist_list[0][playlist_name]
    else:
        playlist_id = "Unknown"
    return playlist_id

def getTrackIDs(user, playlist_id):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

def getTrackFeatures(id):
    meta = sp.track(id)
    name = meta['name']
    artist = meta['album']['artists'][0]['name']
    track = [name, artist]
    return track

def track_identify(ids):
    tracks = []
    for i in range(len(ids)):
      #time.sleep(.5)
      track = getTrackFeatures(ids[i])
      print("Details for id: {} - {}".format(i,track))
      tracks.append(track)
    return tracks

def track_checker(song_list,playlist_list):
    new_list = []
    for song in song_list:
        if song not in playlist_list:
            new_list.append(song)
    return new_list

spotify_pl_name = "Ultimate Classic Rock - Top 50 Prog Rock Songs"
spotify_songs = spotify_song_check(song_list)
create_playlist(spotify_pl_name,cred.user_id)
playlist_names = playlist_names_ids(cred.user_id)
playlist_id = find_playlist_id(playlist_names, spotify_pl_name)
current_tracks_in_playlist = getTrackIDs(cred.user_id,playlist_id)
track_ids = track_identify(current_tracks_in_playlist)

check_songs = track_checker(spotify_songs[1],current_tracks_in_playlist)

def add_songs_playlist(playlist,songs):
    if not songs:
        print("No Songs to add to playlist")
    else:
        sp.playlist_add_items(playlist, songs)

add_songs_playlist(playlist_id,check_songs)