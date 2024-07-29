import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class URLValidationError(Exception):
    pass

def fetch_song_info(url: str) -> dict:
    """
    Fetch song information from a given URL.
    
    :param url: The URL of the webpage containing song information
    :return: A dictionary containing song title, image URL, and description
    """
    if not is_valid_url(url):
        raise URLValidationError("Invalid URL provided")

    try:
        with requests.Session() as session:
            response = session.get(url, timeout=10)
            response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to fetch URL: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    song_info = {
        'title': get_metadata(soup, "og:title"),
        'image_url': get_metadata(soup, "og:image"),
        'description': get_metadata(soup, "og:description"),
    }

    # If we couldn't find Open Graph metadata, try other common tags
    if not song_info['title']:
        song_info['title'] = soup.title.string if soup.title else ""

    return song_info

def get_metadata(soup: BeautifulSoup, property_name: str) -> str:
    meta_tag = soup.find("meta", property=property_name)
    return meta_tag["content"] if meta_tag else ""

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False