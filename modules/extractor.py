from bs4 import BeautifulSoup
import re

def get_tracks_number(response):
    soup = BeautifulSoup(response, 'html.parser')
    number_spans = soup.find_all('span', style="font-size: 18px;color: green;")
    numbers = []
    for number_span in number_spans:
        number_text = number_span.get_text(strip=True)
        match = re.match(r"(\d+):", number_text)
        if match:
            numbers.append(match.group(1))
    return numbers

def extract_urls(response):
    soup = BeautifulSoup(response, 'html.parser')
    hidden_inputs = soup.find_all('input', type='hidden')
    track_urls = []
    for input_tag in hidden_inputs:
        url = input_tag.get('value')
        if url and re.match(r'https?://.*track', url):
            track_urls.append(url)
    return track_urls

def get_tracks_and_artists(response):
    track_numbers = get_tracks_number(response)
    soup = BeautifulSoup(response, 'html.parser')
    track_urls = extract_urls(response)
    grid_items = soup.find_all('div', class_='grid-text')
    album_data = []
    track_index = 0
    for grid_item in grid_items:
        span_tag = grid_item.find('span')
        if span_tag:
            span_tag.attrs.pop('style', None)
            album_name = span_tag.get_text(strip=True)
            artist_name = grid_item.find('br').next_sibling.strip() if grid_item.find('br') else ''
            if album_name and (not album_name[0].isdigit() or ':' not in album_name):
                track_data = {
                    "track_name": album_name,
                    "artist_name": artist_name
                }
                if track_index < len(track_numbers):
                    track_data["track_number"] = track_numbers[track_index]
                    track_index += 1
                if track_index <= len(track_urls):
                    track_data["track_url"] = track_urls[track_index - 1]
                album_data.append(track_data)
    return album_data