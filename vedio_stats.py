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
            
            for item in data.get('items', []):  
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
                
            pageToken = data.get('nextPageToken')
            
            if not pageToken:
                break

        return video_ids
    
    except requests.exceptions.RequestException as e:
        raise e


def extract_video_data(video_ids):
    extracted_data = []
    
    def batch_list(video_id_lst, batch_size):
        for i in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[i:i + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)
            
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails,snippet,statistics&id={video_ids_str}&key={API_KEY}"

            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            
            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
                
                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount": statistics.get('viewCount'),
                    "likeCount": statistics.get('likeCount'),
                    "commentCount": statistics.get('commentCount')
                }
                
                extracted_data.append(video_data)
        
        return extracted_data
                
    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_videoids(playlist_id)
    print(extract_video_data(video_ids))
