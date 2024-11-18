from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from colorama import Fore, Style
from modules.logging import setup_logging
from modules.core import setup_driver
from modules.downloader import drm_downloader
import os

logging = setup_logging()

def extract_title(response):
    soup = BeautifulSoup(response, 'html.parser')
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        title = title.split('|')[0].strip()
        if ' by ' in title:
            track_name, artist = title.split(' by ', 1)
            track_name = track_name.strip()
            artist = artist.strip()
            return track_name, artist
        return title, None
    return None, None

def extract_m3u8(response):
    soup = BeautifulSoup(response, 'html.parser')
    m3u8_link_tag = soup.find('a', id='m3u8Link')
    if m3u8_link_tag and m3u8_link_tag.has_attr('href'):
        return m3u8_link_tag['href']
    return None

def fetching_soundcloud(url):
    try:
        options = Options()
        extension_path = r"extension\2.0.4_0.crx"
        options.add_extension(extension_path)
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-webgl")
        options.add_argument('--enable-unsafe-swiftshader')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'm3u8Link')))
        page_source = driver.page_source
        
        title = extract_title(page_source)
        manifest = extract_m3u8(page_source)

        print(f"{Fore.YELLOW}[SoundCloud-Downloader]:")
        print(f'{Fore.MAGENTA}.++' + '=' * 70 + '++.' + Fore.RESET)
        if title and manifest:
            track_name, artist = title
            print(f"{Fore.YELLOW}TRACK {Fore.RED}     : {Fore.GREEN}{track_name}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}ARTIST     {Fore.RED}: {Fore.GREEN}{artist}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}MANIFEST  {Fore.RED} : {Fore.GREEN}{manifest}{Style.RESET_ALL}")
            return drm_downloader(manifest, track_name)
        else:
            print(f"{Fore.RED}No track data found.{Style.RESET_ALL}")
            return None, None
    except Exception as e:
        print(f"{Fore.RED}Error occurred: {e}{Style.RESET_ALL}")
    finally:
        driver.quit()

