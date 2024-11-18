import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style
from bs4 import BeautifulSoup
from modules.downloader import convert_high_quality, common_downloader
from modules.core import setup_driver
from modules.logging import setup_logging
import os, time
import sys
import logging
import contextlib

logging = setup_logging()

@contextlib.contextmanager
def suppress_stdout_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

def extractor(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    track_name = soup.find("span", {"id": "track_name"}).text if soup.find("span", {"id": "track_name"}) else "Unknown Track"
    artist = soup.find("span", {"id": "artist"}).text if soup.find("span", {"id": "artist"}) else "Unknown Artist"
    return {'track_name': track_name, 'artist': artist}

def fetching_applemusic(url):
    for browser in ['edge', 'firefox', 'chrome', 'brave']:
        with suppress_stdout_stderr():
            driver = setup_driver(browser)
        
        if driver:
            try:
                driver.get("https://aplmate.com/")
                input_field = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "url"))
                )
                input_field.send_keys(url)

                download_button = driver.find_element(By.ID, "send")
                download_button.click()
                time.sleep(5)

                mp3_download_link = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@class='abuttons']/a[@class='abutton is-success is-fullwidth']")
                    )
                )

                download_url = mp3_download_link.get_attribute("href")
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                title = soup.find("h3", itemprop="name").text.strip()
                artist = soup.find("p").find("span").text.strip()

                print()
                print(f"{Fore.RED}NUM   | TRACK NAME                    | ARTIST                    | TRACK URL{Fore.RESET}")
                print(f'{Fore.MAGENTA}.++' + '=' * 170 + '++.' + Fore.RESET)
                print(f"{Fore.GREEN}1     | {title: <30} | {artist: <25} | {download_url}{Fore.RESET}")
                print(f'{Fore.MAGENTA}.++' + '=' * 170 + '++.' + Fore.RESET)

                filename = f"{title}_{artist}.mp3".replace(" ", "_")
                logging.info(f"Formatted filename: {filename}")

                if download_url:
                    logging.info("Downloading the MP3 file.")
                    common_downloader(download_url, filename)
                    break
                else:
                    logging.error("No download URL found.")

            except Exception as e:
                logging.error(f"An error occurred: {e}")

            finally:
                driver.quit()
