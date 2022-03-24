import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from youtubesearchpython import VideosSearch

client_id = ""
client_secret = ""

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))

playlist_id = sys.argv[1]
track_names = [x["track"]["name"] for x in sp.playlist_tracks(playlist_id)["tracks"]["items"]]

for i in track_names:
    video = VideosSearch(i, limit = 1)
    videoID = video.result()["result"][0]["id"]
    videoLINK = f"https://www.youtube.com/watch?v={videoID}"
    print(videoLINK)

    yt = YouTube(videoLINK)
    vid = yt.streams.filter(only_audio=True).first()
    out_file = vid.download(output_path=f"./{sp.playlist(playlist_id)['name']}")

    base, ext = os.path.splitext(out_file)
    new_file = base + ".mp3"
    os.rename(out_file, new_file)

    print(yt.title + " has been successfully downloaded.")
