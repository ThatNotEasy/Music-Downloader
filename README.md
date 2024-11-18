# Music Downloader 🎵
- Music Downloader is an automated tool designed to download and convert music from platforms like Apple Music. Leveraging Selenium and other supporting libraries, this application fetches song information, downloads files in MP3 format, and converts them to high-quality FLAC format.

# Key Features 🚀
- Automated Music Download: Using Selenium to interact with the music source site, the application allows users to input an Apple Music URL and download the track automatically.
- Metadata Extraction: The tool extracts song metadata, such as title and artist, directly from the source page, ensuring each downloaded file is complete with detailed information.
- High-Quality Conversion: Downloaded MP3 files can be converted to FLAC format using ffmpeg for improved audio quality.
- Structured Logging: Each process includes logging to provide detailed feedback on download status, conversion, and error handling.

# Technologies Used 🛠️
- Python: The primary programming language for automation and file management.
- Selenium: Controls the browser to interact with the music source site.
- BeautifulSoup: Parses HTML to retrieve song data.
- ffmpeg: Used for audio conversion from MP3 to FLAC (requires separate installation).

# How to Use 📖
- Clone the Repository:

```bash
$ git clone https://github.com/ThatNotEasy/Music-Downloader.git
$ cd Music-Downloader
```

- Install Dependencies: Make sure ffmpeg is installed and added to your system PATH.

```bash
pip install -r requirements.txt
```

- Run the Program: Enter the URL of a song from Apple Music, and the program will handle the download and conversion automatically.

```bash
python main.py -u "album/tracks url"
```

# Notes ⚠️
- ffmpeg must be installed and added to your PATH for FLAC conversion to work correctly. Download it from the official ffmpeg website.
- Ensure that you’re using compatible versions of Selenium and the browser driver to match your browser version.

# Contributing 🤝
- Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request to propose any changes.
