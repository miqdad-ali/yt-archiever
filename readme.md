# YouTube Channel Archiver

This Python script downloads all videos from a specified YouTube channel and saves them along with their descriptions, thumbnails, and metadata. The script is multi-threaded to speed up the download process.

## Requirements

- Python 3.6+
- `ffmpeg` or `avconv` command-line tool, check https://ffmpeg.org/download.html for detailed instructions

## Usage 

- Run `pip install -r requirments.txt` to install dependencies
- edit the .env file and fill in the values. for video ID, click on any video on the channel you want to archieve, and grab the ID from the url
- run `python main.py`