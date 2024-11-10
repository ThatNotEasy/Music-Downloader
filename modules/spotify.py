from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore
from modules.downloader import spotify_downloader
from modules.extractor import extract_urls, get_tracks_and_artists

init(autoreset=True)

def fetching_spotify(url):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-webgl")
        options.add_argument('--enable-unsafe-swiftshader')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://spotifymate.com/")
        input_url = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "url")))
        
        if input_url:
            input_url.send_keys(url)
        else:
            print(f"{Fore.RED}Error: URL input field not found!")
            return

        download_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "send")))
        download_button.click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "grid-container")))
        page_source = driver.page_source
        track_urls = extract_urls(page_source)
        data = get_tracks_and_artists(page_source)
        
        if data:
            print(f"{Fore.YELLOW}[Spotify-Downloader]: {Fore.RED}NUM   | {Fore.RED}TRACK NAME                    | {Fore.RED}ARTIST                    | {Fore.RED}TRACK URL{Fore.RESET}")
            print(f'{Fore.MAGENTA}.++' + '=' * 170 + '++.' + Fore.RESET)
            for idx, track in enumerate(data):
                track_url = track_urls[idx] if idx < len(track_urls) else "N/A"
                print(f"{Fore.YELLOW}[Spotify-Downloader]: {Fore.RED}{track['track_number']: <4} {Fore.WHITE}| "
                      f"{Fore.GREEN}{track['track_name']: <30} {Fore.WHITE}| "
                      f"{Fore.GREEN}{track['artist_name']: <25} {Fore.WHITE}| "
                      f"{Fore.GREEN}{track_url}{Fore.RESET}")
                print(f'{Fore.MAGENTA}.++' + '=' * 170 + '++.' + Fore.RESET)

                # Download each track
                spotify_downloader(track_url, track['track_name'], track['artist_name'])
                
        else:
            print(f"{Fore.RED}No track data found.")
    except Exception as e:
        print(f"{Fore.RED}Error occurred: {e}")
    finally:
        driver.quit()