import requests
import json
import os 
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv(dotenv_path='./.env')
API_KEY = os.getenv("API_KEY")
channel_handle = "MrBeast"
maxResults = 50


def get_playlist_id():
    """
    Get the Uploads Playlist ID for a channel using channel handle.
    """
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        channel_items = data['items'][0]
        channel_playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        print("Uploads Playlist ID:", channel_playlist_id)
        return channel_playlist_id

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
    except ValueError:
        print("Response is not valid JSON")
    except KeyError:
        print("Unexpected JSON structure")


def get_videoids(playlist_id): 
    """
    Get all video IDs from a given playlist (uploads playlist).
    """
    video_ids = []
    pageToken = None

    try:
        while True:
            url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}"
            
            if pageToken:
                url += f"&pageToken={pageToken}"
            
            response = requests.get(url)
            response.raise_for_status()  

            data = response.json()
            
            for item in data.get('items', []):  # ✅ fixed: items not item
                video_id = item['contentDetails']['videoId']  # ✅ fixed: videoId not video_id
                video_ids.append(video_id)
                
            pageToken = data.get('nextPageToken')
            
            if not pageToken:
                break

        return video_ids
    
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    if playlist_id:
        video_ids = get_videoids(playlist_id)
        print("Total videos fetched:", len(video_ids))
        print(video_ids[:902])  # show first 10 video IDs
