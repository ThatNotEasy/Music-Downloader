import os
import sys
import argparse
import platform
from colorama import Fore
from modules.banners import banners
from modules.spotify import fetching_spotify
from loguru import logger

def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Spotify Downloader")
    parser.add_argument('-u', '--url', help="The Spotify album or track URL")
    parser.add_argument('-f', '--file', help="A file containing a list of Spotify album/track URLs, one per line")
    return parser.parse_args()

def download_from_url(url):
    """Download music from a Spotify URL."""
    logger.info(f"Downloading from URL: {url}")
    fetching_spotify(url)
    print(f"{Fore.GREEN}Downloaded: {url}")

def download_from_file(file_path):
    """Download music from a file containing Spotify URLs."""
    if not os.path.isfile(file_path):
        logger.error(f"File {file_path} does not exist.")
        print(f"{Fore.RED}Error: File {file_path} does not exist.")
        return

    with open(file_path, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()
            if url:
                download_from_url(url)
            else:
                logger.warning("Skipped empty line or invalid URL format.")

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
    logger.add("spotify_downloader.log", format="{time} {level} {message}", level="INFO", rotation="10 MB")
    main()
