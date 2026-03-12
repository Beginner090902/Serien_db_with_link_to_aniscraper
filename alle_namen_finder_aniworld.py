import itertools
from db_manager import DBManager
from tqdm import tqdm
import cProfile
import pstats
start = "https://aniworld.to/animes/"

table_anime_namen = "anime_namen"

db = DBManager("aniworld.db")

db.create_table(table_name=table_anime_namen)


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def crawl_depth_1(start_url):
    found_urls = set()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(start_url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for a in soup.find_all("a", href=True):
        href = a.get("href")
        if not isinstance(href, str):
            continue

        href = href.strip()

        if href.startswith(("mailto:", "javascript:", "tel:", "#")):
            continue

        absolute_url = urljoin(start_url, href)

        parsed = urlparse(absolute_url)
        if parsed.scheme in ("http", "https"):
            if "/stream/" in absolute_url:
                absolute_url = absolute_url.replace("https://aniworld.to/anime/stream/", "")
                found_urls.add(absolute_url)

    return found_urls


if __name__ == "__main__":
    urls = crawl_depth_1(start)

    with tqdm(total=len(urls)) as pbar:
        for u in sorted(urls):
            finde_url_in_data_base = db.find_by_title_in_table(table_name=table_anime_namen,such_url=u)
            if not finde_url_in_data_base:
                db.add_such_url_in_table(such_url=u,table_name=table_anime_namen)
            pbar.update()

    db.close()

