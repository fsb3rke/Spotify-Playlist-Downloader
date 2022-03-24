import os
import sys
from tkinter.filedialog import askdirectory
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from youtubesearchpython import VideosSearch
from colorama import Fore, Style

os.system("color")

client_id = ""
client_secret = ""

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))

playlist_id = sys.argv[1]
track_names = [x["track"]["name"] for x in sp.playlist_tracks(playlist_id)["tracks"]["items"]]

directory = askdirectory()

for i in range(len(track_names)):
    try:
        video = VideosSearch(track_names[i], limit = 1)
        videoID = video.result()["result"][0]["id"]
        videoLINK = f"https://www.youtube.com/watch?v={videoID}"
        print("\n"+Fore.YELLOW+videoLINK+Style.RESET_ALL)

        yt = YouTube(videoLINK)
        vid = yt.streams.filter(only_audio=True).first()
        out_file = vid.download(output_path=f"{directory}/{sp.playlist(playlist_id)['name']}")

        base, ext = os.path.splitext(out_file)
        new_file = base + ".mp3"
        os.rename(out_file, new_file)

        print(f" {Fore.MAGENTA}{str(i+1)}/{str(len(track_names))}{Style.RESET_ALL} {Fore.GREEN}{yt.title} has been successfully downloaded.{Style.RESET_ALL}\n")
    except:
        print(f" {Fore.MAGENTA}{str(i+1)}/{str(len(track_names))}{Style.RESET_ALL} {Fore.RED}{yt.title} hasn't been successfully downloaded.{Style.RESET_ALL}\n")
