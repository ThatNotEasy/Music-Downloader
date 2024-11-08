from bs4 import BeautifulSoup
import re

def detect_artist_name(text):
    match = re.search(r'([A-Z]+)([A-Z][a-z].*)', text)
    if match:
        title = match.group(1)
        artist_name = match.group(2)
        artist_name = artist_name.strip().title()
        artist_name = artist_name.replace(" ", "_")
        return title, artist_name
    else:
        return None, None

def extractor(response):
    soup = BeautifulSoup(response, 'html.parser')
    songs = soup.find_all('div', class_='grid-container')
    track_data = []
    
    for song in songs:
        try:
            form = song.find('form')
            token_input = form.find('input', {'name': 'token'}) if form else None
            token = token_input.get('value') if token_input else None

            track_number = song.find('div', class_='grid-text').get_text(strip=True)
            title_and_artist = song.find_all('div', class_='grid-text')[1].get_text(strip=True)
            download_button = form.find('input', {'name': 'track'}) if form else None
            download_link = download_button['value'] if download_button else None

            if track_number and title_and_artist and token:
                title, artist = detect_artist_name(title_and_artist)
                track_data.append((track_number, title, artist, download_link, token))
            else:
                print(f"Error: Missing essential data for track: {track_number}")

        except Exception as e:
            print(f"Error processing song: {e}")
    
    return track_data


def extract_content(response):
    response_text = response.decode('utf-8')
    mp3_url_pattern = r'https://api\.spotifymate\.com/[^\s]*\.mp3[^\s]*'
    cover_url_pattern = r'https://spotifymate\.com/dl\?url=[^&]*&title=[^&]*'
    mp3_urls = re.findall(mp3_url_pattern, response_text)
    cover_urls = re.findall(cover_url_pattern, response_text)
    if not mp3_urls:
        print("No MP3 URLs found.")
    if not cover_urls:
        print("No cover URLs found.")
    return mp3_urls, cover_urls