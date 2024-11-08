import os
import sys
import argparse
import platform
from colorama import Fore
from modules.banners import banners
from modules.spotify import spotify_downloader, fetching_spotify

def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Spotify Downloader")
    parser.add_argument('-u', '--url', required=False, 
                        help="The Spotify album or track URL")
    parser.add_argument('-f', '--file', required=False, 
                        help="A file containing a list of Spotify album/track URLs, one per line")
    return parser.parse_args()

def download_from_url(url):
    print(f"Downloading from URL: {url}...")
    album_url, track_data = fetching_spotify(url)

    if track_data:
        for track in track_data:
            track_number, title, artist, download_link, token = track
            print(f"{Fore.RED}[DOWNLOADER]: {Fore.GREEN}{title} {Fore.YELLOW}BY {Fore.GREEN}{artist}...")
            spotify_downloader(download_link)
    else:
        print(f"{Fore.RED}Error: No valid track data found for {url}.")

def download_from_file(file_path):
    """Download music from a file containing Spotify URLs."""
    if not os.path.isfile(file_path):
        print(f"{Fore.RED}Error: File {file_path} does not exist.")
        return

    with open(file_path, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()
            if url:
                download_from_url(url)

def main():
    clear_terminal()
    banners()
    args = parse_args()

    if args.url:
        download_from_url(args.url)

    elif args.file:
        download_from_file(args.file)

    else:
        print(f"{Fore.RED}Error: You must provide either a URL or a file with URLs.")
        sys.exit(1)

if __name__ == "__main__":
    main()