# YouTube Channel Archiver

This Python script downloads all videos from a specified YouTube channel and saves them along with their descriptions, thumbnails, and metadata. The script is multi-threaded to speed up the download process.

## Requirements

- Python 3.6+
- `ffmpeg` or `avconv` command-line tool, check https://ffmpeg.org/download.html for detailed instructions
- YouTube Data API, you will need to enable the API and get your key. check https://developers.google.com/youtube/v3/getting-started

## Usage 

- Run `pip install -r requirments.txt` to install dependencies
- edit the .env file and fill in the values. for video ID, click on any video on the channel you want to archieve, and grab the ID from the url. this will be used to fetch all content (live streams, shorts, videos)
- run `python main.py`

## TODO

- Store jobs in an sqlite DB, this would allow users to resume donwloading content at any time. This would also help organize content & jobs for multiple channels
- Nice(r) console prints for checking progress 