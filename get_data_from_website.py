from time import time
import requests
from bs4 import BeautifulSoup
from db_manager import DBManager
from tqdm import tqdm
from urllib.parse import urljoin,urlparse
import time
db_file="instance/aniworld.db"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_all_url_names(start_url):
    found_urls = []

    response = requests.get(start_url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        if "ani" in start_url:
            if not a.get('title') == None:
                name = a.get('title')
                name = name.replace(" Stream anschauen","")
             
        if "s.to" in start_url:
            if not a.text == None:
                name = a.text
                
        #print(f"Tag: {a.name}")
        #print(f"Alle Attribute: {a.attrs}")
        #print(f"HTML: {a}")
        if not isinstance(href, str):
            continue

        href = href.strip()

        if href.startswith(("mailto:", "javascript:", "tel:", "#")):
            continue
        
        if not ("/serie/" in href or "/anime/" in href):
            continue
        if "/serie/" in href:
            href = href.replace("/serie/", "")
        if "/stream/" in href:
            href = href.replace("/anime/stream/","")

        found_urls.append((href,name))
        #found_names.add(name)

    sorted_urls = sorted(found_urls)
    #print(sorted_urls)
    return sorted_urls

def add_all_urls_and_name_in_table(list:set|list,table_name:str):
    db = DBManager(db_file)
    with tqdm(total=len(list)) as pbar:
        for u in list:
            #print(u)
            finde_url_in_data_base = db.find_by_title_in_table(table_name=table_name,such_url=u[0])
            if not finde_url_in_data_base:
                db.add_such_url_in_table(such_url=u[0],table_name=table_name)
            db.add_real_name_on_url_in_table(real_name=u[1],such_url=u[0],table_name=table_name)
            pbar.update()
            time.sleep(0.001)
    db.close()
    return f"Updated all urls in {table_name}"

def get_year_and_name(start_url:str,such_url:str) -> str:
    if "aniworld" in start_url:
        full_url = f"{start_url}stream/{such_url}"
        response = requests.get(full_url, headers=headers, timeout=100)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        jahr_start = soup.find("span", itemprop="startDate").find("a").text.strip()
        jahr_ende = soup.find("span", itemprop="endDate").find("a").text.strip()
        jahr_zusammen= f"{jahr_start}-{jahr_ende}"

        img = soup.find("img", itemprop="image")
        img_url_intern = img.get("data-src")
        img_url = urljoin(start_url, img_url_intern)

    elif"s.to" in start_url:
        full_url = f"{start_url}{such_url}"
        #print(f"full url {full_url}")
        response = requests.get(full_url, headers=headers, timeout=100)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        jahr_anzeige = soup.find("p")
        jahr_start = jahr_anzeige.find("a","small text-muted").text.strip()
        #print(f"Jahr start {jahr_start}")
        jahr_ende = jahr_anzeige.find_next("a","small text-muted").text.strip()
        #print(f"Jahr ende {jahr_ende}")
        jahr_zusammen= f"{jahr_start}-{jahr_ende}"
        #print(f"Jahr zusammen {jahr_zusammen}")

        img_grob_gefunden = soup.find("div","d-md-none float-end text-end show-cover-mobile")
        img = img_grob_gefunden.find("img")
        img_url_intern = img.get('data-src')
        img_url = urljoin(start_url, img_url_intern)
    
    return jahr_zusammen,img_url



def add_year_and_img(start_url:str,table_name:str):
    db = DBManager(db_file)
    list_of_all_anime = db.get_all_in_table(table_name=table_name)

    print("Update all year and Images stamps ")
    with tqdm(total=len(list_of_all_anime)) as pbar:
        for anime_url in list_of_all_anime:
            #print(anime_url[3])
            if (anime_url[3] == None) or (anime_url[4] == None):
                anime_year_and_name = get_year_and_name(start_url=start_url,such_url=anime_url[1])
                db.add_year_in_table(table_name=table_name,such_url=anime_url[1],year=anime_year_and_name[0])
                db.add_image_in_table(table_name=table_name,such_url=anime_url[1],image_url=anime_year_and_name[1])
                time.sleep(1)
            pbar.update()
            time.sleep(0.001)
            
    db.close()
    return f"Update Years and Images erfolgreich in {table_name}"


