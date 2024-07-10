import requests, json
from googleapiclient.discovery import build

API_Key = "AIzaSyDJGl1zNWZR8XzbwIjk81XPGRWosK4wFp4"


def trend_vidlinksfetch():
    videometa = []

    url = "https://www.searchapi.io/api/v1/search"

    params = {
        "engine": "youtube_trends",
        "api_key": "yUcsHBZx1hYV96S8Yvs97BVF",
        
    }

    response = requests.get(url, params = params)
    print(response)
    response = response.json()
    print(response)
    trending_vids = response["recently_trending"]
    for video in trending_vids:
        videometa.append([video["title"], video["link"], video["length"], video["channel"]["title"]])

    return videometa 

def fetch_vidmeta(link):
    youtube = build("youtube","v3",developerKey=API_Key)
    VidId  = link.split('/')[3]

    request = youtube.search().list(
        part = "snippet",
        videoId = VidId,

    )