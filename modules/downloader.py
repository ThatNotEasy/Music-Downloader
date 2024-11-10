import os, requests, json, subprocess
from colorama import Fore, Style
from modules.logging import setup_logging
from tqdm import tqdm
from modules.banners import banners

logging = setup_logging()

def drm_downloader(url, save_name):
    save_dir = 'content/'
    os.makedirs(save_dir, exist_ok=True)

    command = (
        f'N_m3u8DL-RE.exe "{url}" '
        f'--auto-select --save-dir "{save_dir}" '
        f'-mt --save-name "{save_name}" '
        f'--header "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0" '
        f'--header "Referer: {url}"'
    )

    try:
        exit_code = os.system(command)
        if exit_code == 0:
            logging.info(f"Download completed successfully and saved as {save_name} in {save_dir}")
            current_file = os.path.join(save_dir, f"{save_name}.m4a")
            new_file_convert = os.path.join(save_dir, f"{save_name}.flac")
            convert_high_quality(current_file, new_file_convert)
        else:
            logging.error(f"Command failed with exit code {exit_code}")
    except Exception as e:
        logging.error(f"Error during download: {e}")

def spotify_downloader(url, track_name, artist_name):
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
    if not url:
        print(f"{Fore.RED}Error: No data returned from fetching_spotify.")
        return

    params = {'url': url}
    response = requests.get('https://tatsumi-crew.net/API/spotify.php', params=params, cookies=cookies, headers=headers)
    
    try:
        json_data = response.json()
        download_url = json_data['urlDownload']
        song_name = json_data['song_name']
        artist_name = json_data['artist']
    except (ValueError, KeyError) as e:
        print(f"{Fore.RED}Error parsing response: {e}")
        return

    if not os.path.exists("content"):
        os.makedirs("content")
    
    if download_url:
        with requests.get(download_url, headers=headers, cookies=cookies, stream=True) as sec_response:
            if sec_response.status_code == 200:
                total_size = int(sec_response.headers.get('content-length', 0))
                new_track_name = track_name.replace(" ", "_")
                new_artist_name = artist_name.replace(" ", "_")
                file_path = f"content/{new_track_name}_{new_artist_name}.m4a"
                
                with open(file_path, 'wb') as f, tqdm(
                    desc=f"Downloading {song_name} by {artist_name}",
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    colour='green'
                ) as progress_bar:
                    for chunk in sec_response.iter_content(chunk_size=1024):
                        f.write(chunk)
                        progress_bar.update(len(chunk))
                
                print(f"{Fore.GREEN}Download successful! File saved as '{file_path}\n'")
                current_file = f"{new_track_name}_{new_artist_name}.m4a"
                new_file_convert = f"{new_track_name}_{new_artist_name}.flac"
                convert_high_quality(current_file, new_file_convert)
            else:
                print(f"{Fore.RED}Error: Download failed. Status code: {sec_response.status_code}")
    else:
        print(f"{Fore.RED}Error: No download URL found.")


def convert_high_quality(input_file, output_file):
    output_format = "flac"  # Default format
    sample_rate = 96000     # Default sample rate
    bit_rate = "320k"       # Default bit rate

    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("FFmpeg is not installed or not found. Please install FFmpeg first.")
        return

    # Remove quotes from the input and output paths, as subprocess will handle spaces correctly
    input_file = input_file  # No need to add quotes
    output_file = output_file  # No need to add quotes

    if output_format.lower() == "flac":
        command = [
            "ffmpeg", "-i", input_file, 
            "-acodec", "flac", 
            "-ar", str(sample_rate), 
            "-sample_fmt", "s32", 
            output_file
        ]
    elif output_format.lower() == "mp3":
        command = [
            "ffmpeg", "-i", input_file, 
            "-acodec", "libmp3lame", 
            "-ab", bit_rate, 
            "-ar", str(sample_rate), 
            output_file
        ]
    elif output_format.lower() == "wav":
        command = [
            "ffmpeg", "-i", input_file, 
            "-ar", str(sample_rate), 
            "-sample_fmt", "s32", 
            output_file
        ]
    else:
        print(f"Unsupported format: {output_format}. Please choose 'flac', 'mp3', or 'wav'.")
        return

    try:
        print(f"Converting {input_file} to {output_format} with sample rate {sample_rate}Hz...")
        subprocess.run(command, check=True)
        print(f"Conversion complete! Output file: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")