from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore
import requests, json
from modules.extractor import extractor, extract_content

init(autoreset=True)

def fetching_spotify(url):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        driver.get("https://spotifymate.com/")

        input_url = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "url")))

        if input_url:
            input_url.send_keys(url)
        else:
            print(f"{Fore.RED}Error: URL input field not found!")
            return None, None

        download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "send")))
        download_button.click()

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "grid-container")))

        page_source = driver.page_source
        track_data = extractor(page_source)

        if track_data:
            for track in track_data:
                track_number, title, artist, download_link, token = track
                print(f"{Fore.YELLOW}Track:{Fore.GREEN} {track_number}")
                print(f"{Fore.YELLOW}Title:{Fore.GREEN} {title}")
                print(f"{Fore.YELLOW}Artist:{Fore.GREEN} {artist}")
                print(f"{Fore.YELLOW}Token:{Fore.GREEN} {token}")
                print(f"{Fore.YELLOW}Download Link:{Fore.GREEN} {download_link}")
                print('-' * 40)
            return url, track_data
        else:
            print(f"{Fore.RED}Error: Failed to extract valid data.")

    except Exception as e:
        print(f"{Fore.RED}Error occurred: {e}")
    finally:
        driver.quit()


def spotify_downloader(url):
    cookies = {
        'cf_clearance': 'yae64EVM9IoaImZw4E_9Gt9I1Buo__njjzF6xOg2Vpw-1731033213-1.2.1.1-NrO_ZMAV5PRmAPi6IEiwZ88H32_VkldEodnokrKqDVa6P6XfY8txrK1_l5Ma4PqN3_TOjXsjQL9svFJ.oUV.BnhbTg2_MXz7NTmDllKF9QIjSGw0p1Ytmoa9D7zT_eqlak_W0KYhPPuO7aT_ufyAxpbeBXP.FLWmng6SiHaLx11CgereLibTRlJO4YIwBctJvEMlX8g1ZoNB2A5KgD9C.lmq6ALWj.ZeNur6Jlria.w6XXE35A7zYxPnnxShxf0j827OsHkx95qg8o4_UInIbOMbTyPJCxgisFqGkaKSsY.uSsvWZqPDzDynVA7vDyfdo3fs54tvsbLeJ61WMQnVCzzFPPI5PP_zDiTUhvGD2HntHRRvU2gPxeG1hYyRBnuIFpmTn1f4IjXhG4m4B3iTfBCKQedBCKVYTvK_2KsgjTEQkoG9E1OktIO11OIKIY6J',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': 'cf_clearance=yae64EVM9IoaImZw4E_9Gt9I1Buo__njjzF6xOg2Vpw-1731033213-1.2.1.1-NrO_ZMAV5PRmAPi6IEiwZ88H32_VkldEodnokrKqDVa6P6XfY8txrK1_l5Ma4PqN3_TOjXsjQL9svFJ.oUV.BnhbTg2_MXz7NTmDllKF9QIjSGw0p1Ytmoa9D7zT_eqlak_W0KYhPPuO7aT_ufyAxpbeBXP.FLWmng6SiHaLx11CgereLibTRlJO4YIwBctJvEMlX8g1ZoNB2A5KgD9C.lmq6ALWj.ZeNur6Jlria.w6XXE35A7zYxPnnxShxf0j827OsHkx95qg8o4_UInIbOMbTyPJCxgisFqGkaKSsY.uSsvWZqPDzDynVA7vDyfdo3fs54tvsbLeJ61WMQnVCzzFPPI5PP_zDiTUhvGD2HntHRRvU2gPxeG1hYyRBnuIFpmTn1f4IjXhG4m4B3iTfBCKQedBCKVYTvK_2KsgjTEQkoG9E1OktIO11OIKIY6J',
        'priority': 'u=1, i',
        'referer': 'https://tatsumi-crew.net/spotify/?fbclid=IwZXh0bgNhZW0CMTAAAR0501peCxKFyVwoezhtkGpmX6DonxHPQgcz_Ut-9w0SmQpEzwElTOWS814_aem_yGn_SF_xlQeKbzMUeK9cOg',
        'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"130.0.2849.68"',
        'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.92", "Microsoft Edge";v="130.0.2849.68", "Not?A_Brand";v="99.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    }

    params = {'url': url,}
    response = requests.get('https://tatsumi-crew.net/API/spotify.php', params=params, cookies=cookies, headers=headers)
    data = response.text
    json_data = json.loads(data)
    download_url = json_data['urlDownload']
    song_name = json_data['song_name']
    artist_name = json_data['artist']
    # album_name = json_data['album']
    
    if download_url:
        sec_response = requests.get(download_url, headers=headers, cookies=cookies)
        if sec_response.status_code == 200:
            with open(f"{song_name}_{artist_name}.mp3", 'wb') as f:
                f.write("content/" + sec_response.content)
            print(f"{Fore.GREEN}Download successful! File saved as '{song_name}_{artist_name}.mp3'")
        else:
            print(f"{Fore.RED}Error: Download failed. Status code: {sec_response.status_code}")
    else:
        print(f"{Fore.RED}Error: No download URL found.")