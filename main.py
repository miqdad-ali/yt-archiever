import os
import requests
# from pytube import YouTube
from dotenv import load_dotenv
import subprocess
from concurrent.futures import ThreadPoolExecutor


load_dotenv()

API_KEY = os.getenv("API_KEY")
VIDEO_ID = os.getenv("VIDEO_ID")
SAVE_DIRECTORY = os.getenv("SAVE_DIRECTORY")
NUM_THREADS = int(os.getenv("NUM_THREADS", "5"))


def get_CHANNEL_ID(api_key, video_id):
    base_url = "https://www.googleapis.com/youtube/v3"
    endpoint = f"{base_url}/videos?key={api_key}&id={video_id}&part=snippet"
    response = requests.get(endpoint).json()

    if 'items' not in response:
        print("Error retrieving channel ID.")
        return None

    CHANNEL_ID = response["items"][0]["snippet"]["channelId"]
    return CHANNEL_ID

CHANNEL_ID = get_CHANNEL_ID(API_KEY, VIDEO_ID)
print(f"Channel ID: {CHANNEL_ID}")


def get_video_links(api_key, CHANNEL_ID):
    base_url = "https://www.googleapis.com/youtube/v3"
    endpoint = f"{base_url}/search?key={api_key}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=50"
    video_links = []
    
    while True:
        response = requests.get(endpoint).json()

        if 'error' in response:
            print(f"Error: {response['error']['message']}")
            return []

        if 'items' not in response:
            print(f"Unexpected API response: {response}")
            return []

        for item in response["items"]:
            if item["id"]["kind"] == "youtube#video":
                video_id = item["id"]["videoId"]
                video_links.append(f"https://www.youtube.com/watch?v={video_id}")
                
        if "nextPageToken" in response:
            endpoint = f"{base_url}/search?key={api_key}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=50&pageToken={response['nextPageToken']}"
        else:
            break

    return video_links


def download_video(video_url, save_directory):
    save_path = os.path.join(save_directory, "%(title)s", "%(title)s.%(ext)s")
    command = [
        "yt-dlp",
        "-f",
        "best[ext=mp4]",
        "--write-description",
        "--write-info-json",
        "--write-thumbnail",
        "-o",
        save_path,
        video_url,
    ]
    subprocess.run(command, check=True)

if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

video_links = get_video_links(API_KEY, CHANNEL_ID)

with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    futures = [executor.submit(download_video, video_link, SAVE_DIRECTORY) for video_link in video_links]

    for future in futures:
        try:
            future.result()
        except Exception as e:
            print(f"An error occurred while downloading a video: {e}")

print("All videos downloaded!")