import os
import sys
import argparse
import platform
from colorama import Fore
from modules.banners import banners
from modules.spotify import fetching_spotify
from modules.soundcloud import fetching_soundcloud
from modules.applemusic import fetching_applemusic
from modules.logging import setup_logging

logging = setup_logging()

def clear_terminal():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def parse_args():
    parser = argparse.ArgumentParser(
        description="Music Downloader: Download tracks or albums from Spotify, SoundCloud, or Apple Music using URLs.",
        epilog=(
            "Example usage:\n"
            "  python main.py -u 'https://spotify.com/track/xyz'\n"
            "  python main.py -u 'https://soundcloud.com/artist/song'\n"
            "  python main.py -u 'https://music.apple.com/us/album/blue/123456789'\n"
            "  python main.py -f urls.txt\n\n"
            "URLs in the file (urls.txt) should be one per line, with each line containing a valid Spotify, SoundCloud, or Apple Music URL.\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-u', '--url', 
        help="The album or track URL (Spotify, SoundCloud, or Apple Music)."
             "\nExample: 'https://spotify.com/track/xyz' or 'https://soundcloud.com/artist/song'."
    )
    parser.add_argument(
        '-f', '--file', 
        help="A file containing a list of album/track URLs, one per line."
             "\nEach line should contain a valid Spotify, SoundCloud, or Apple Music URL."
    )
    return parser.parse_args()

def download_from_url(url):
    if 'spotify.com' in url:
        clear_terminal()
        banners()
        logging.info("SPOTIFY SERVICE EXECUTING!")
        fetching_spotify(url)
    elif 'soundcloud.com' in url:
        clear_terminal()
        banners()
        logging.info("SOUNDCLOUD SERVICE EXECUTING!")
        fetching_soundcloud(url)
    elif 'music.apple.com' in url:
        clear_terminal()
        banners()
        logging.info("APPLE MUSIC SERVICE EXECUTING!")
        fetching_applemusic(url)
    else:
        clear_terminal()
        banners()
        logging.warning("Unsupported URL")
        print(f"{Fore.RED}Error: Unsupported URL. Please provide a valid Spotify, SoundCloud, or Apple Music URL.")

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
        print(f"{Fore.WHITE}Error: You must provide either a URL or a file with URLs.\n"
              f"Use -h or --help to see usage information.\n")
        sys.exit(1)

if __name__ == "__main__":
    clear_terminal()
    banners()
    main()