import os
import sys
import argparse
import platform
from colorama import Fore
from modules.banners import banners
from modules.spotify import fetching_spotify
from modules.soundcloud import fetching_soundcloud
from modules.logging import setup_logging

logging = setup_logging()

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def parse_args():
    parser = argparse.ArgumentParser(
        description="Music Downloader: Download tracks from Spotify or SoundCloud using URLs."
    )
    parser.add_argument(
        '-u', '--url', 
        help="The album or track URL (Spotify or SoundCloud). Example: 'https://spotify.com/track/xyz' or 'https://soundcloud.com/artist/song'."
    )
    parser.add_argument(
        '-f', '--file', 
        help="A file containing a list of album/track URLs, one per line. Each line should contain a valid Spotify or SoundCloud URL."
    )
    return parser.parse_args()

def download_from_url(url):
    if 'spotify.com' in url:
        clear_terminal()
        banners()
        fetching_spotify(url)
    elif 'soundcloud.com' in url:
        clear_terminal()
        banners()
        fetching_soundcloud(url)
    else:
        clear_terminal()
        banners()
        logging.warning("Unsupported URL")
        print(f"{Fore.RED}Error: Unsupported URL. Please provide a valid Spotify or SoundCloud URL.")

def download_from_file(file_path):
    if not os.path.isfile(file_path):
        logging.error(f"File {file_path} does not exist.")
        print(f"{Fore.RED}Error: File {file_path} does not exist.")
        return

    with open(file_path, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()
            if url:
                download_from_url(url)
            else:
                logging.warning("Skipped empty line or invalid URL format.")

def main():
    clear_terminal()
    banners()
    args = parse_args()

    if args.url:
        download_from_url(args.url)

    elif args.file:
        download_from_file(args.file)

    else:
        print(f"{Fore.WHITE}Error: You must provide either a URL or a file with URLs. Or see --help\n")
        sys.exit(1)

if __name__ == "__main__":
    clear_terminal()
    banners()
    main()