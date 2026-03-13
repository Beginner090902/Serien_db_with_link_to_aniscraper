import requests
from bs4 import BeautifulSoup
from db_manager import DBManager
from tqdm import tqdm

def get_all_url_names(start_url):
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
    sorted(found_urls)
    return found_urls

def add_all_urls(list:set|list):
    with tqdm(total=len(list)) as pbar:
        for u in urls:
            finde_url_in_data_base = db.find_by_title_in_table(table_name=table_anime_namen,such_url=u)
            if not finde_url_in_data_base:
                db.add_such_url_in_table(such_url=u,table_name=table_anime_namen)
            pbar.update()

def get_year(start_url:str,such_url:str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    full_url = f"{start_url}stream/{such_url}"
    print(full_url)
    response = requests.get(full_url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")


if __name__ == "__main__":
    webseite_url_all_anime = "https://aniworld.to/animes/"
    webseite_url_for_ane_anime = "https://aniworld.to/anime/"
    table_anime_namen = "anime_namen"
    db = DBManager("aniworld.db")

    #db.create_table(table_name=table_anime_namen)
    #all_urls = crawl_depth_1(webseite_url)
    #add_all_urls(all_urls)
    get_year(start_url=webseite_url_for_ane_anime,such_url="07-ghost")

    db.close()

