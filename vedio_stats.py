import requests
import json
import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')
API_KEY = os.getenv("API_KEY")
channel_handle = "MrBeast"

def get_playlist_id():
    url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Correct spelling

        # Parse JSON
        data = response.json()
        # print(json.dumps(data, indent=4))  # Uncomment if you want to see raw data

        channel_items = data['items'][0]
        channel_playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        print("Uploads Playlist ID:", channel_playlist_id)

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
    except ValueError:
        print("Response is not valid JSON")
    except KeyError:
        print("Unexpected JSON structure")

if __name__ == "__main__":
    
    get_playlist_id()

