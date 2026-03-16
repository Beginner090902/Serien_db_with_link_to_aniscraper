import requests
from bs4 import BeautifulSoup
from db_manager import DBManager
from tqdm import tqdm
from urllib.parse import urljoin,urlparse
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_all_url_names(start_url):
    found_urls = set()

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
    sorted_urls = sorted(found_urls)
    return sorted_urls

def add_all_urls(list:set|list):
    print("Add url to db")
    with tqdm(total=len(list)) as pbar:
        for u in list:
            finde_url_in_data_base = db.find_by_title_in_table(table_name=table_anime_namen,such_url=u)
            if not finde_url_in_data_base:
                db.add_such_url_in_table(such_url=u,table_name=table_anime_namen)
            pbar.update()

def get_year(start_url:str,such_url:str) -> str:
    full_url = f"{start_url}stream/{such_url}"
    response = requests.get(full_url, headers=headers, timeout=100)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    jahr_start = soup.find("span", itemprop="startDate").find("a").text.strip()
    jahr_ende = soup.find("span", itemprop="startDate").find("a").text.strip()
    jahr_zusammen= f"{jahr_start}-{jahr_ende}"
    return jahr_zusammen

def get_name(start_url:str,such_url:str):
    full_url = f"{start_url}stream/{such_url}"
    response = requests.get(full_url, headers=headers, timeout=100)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    real_name = soup.find("h1").find("span").text.strip()
    return real_name

def get_image(start_url:str,such_url:str): 
    full_url = f"{start_url}stream/{such_url}"
    response = requests.get(full_url, headers=headers, timeout=100)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    img = soup.find("img", itemprop="image")
    img_url_intern = img.get("data-src")
    img_url = urljoin(start_url, img_url_intern)

    return img_url

def add_year_real_name_imgage_to_db(start_url:str):

    list_of_all_anime = db.get_all_in_table(table_name=table_anime_namen)
    print("Update all Names ")
    with tqdm(total=len(list_of_all_anime)) as pbar:
        for anime_url in list_of_all_anime:
            #print(anime_url[2])
            if anime_url[2] == None: 
                anime_name = get_name(start_url=start_url,such_url=anime_url[1])
                db.add_real_name_on_url_in_table(real_name=anime_name,such_url=anime_url[1],table_name=table_anime_namen)
            pbar.update()
            time.sleep(0.0001)
            

    print("Update all year stamps ")
    with tqdm(total=len(list_of_all_anime)) as pbar:
        for anime_url in list_of_all_anime:
            #print(anime_url[3])
            if anime_url[3] == None:
                anime_year = get_year(start_url=start_url,such_url=anime_url[1])
                db.add_year_in_table(table_name=table_anime_namen,such_url=anime_url[1],year=anime_year)
            pbar.update()
            time.sleep(0.0001)

    print("Update all Images ")
    with tqdm(total=len(list_of_all_anime)) as pbar:
        for anime_url in list_of_all_anime:
            #print(anime_url[4])
            if anime_url[4] == None:
                anime_img_url = get_image(start_url=start_url,such_url=anime_url[1])
                db.add_image_in_table(table_name=table_anime_namen,such_url=anime_url[1],image_url=anime_img_url)
            pbar.update()
            time.sleep(0.0001)

if __name__ == "__main__":
    webseite_url_all_anime = "https://aniworld.to/animes/"
    webseite_url_for_one_anime = "https://aniworld.to/anime/"
    table_anime_namen = "anime_namen"
    db = DBManager("instance/aniworld.db")

    db.create_table(table_name=table_anime_namen)
    all_urls = get_all_url_names(start_url=webseite_url_all_anime)
    add_all_urls(all_urls)
    
    add_year_real_name_imgage_to_db(start_url=webseite_url_for_one_anime)
    db.close()

