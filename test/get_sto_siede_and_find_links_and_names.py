import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
start_url = "https://s.to/serien/"
sto_file_path = "sto.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_sto_html():
    file = open(sto_file_path)
    soup = BeautifulSoup(file, "html.parser")
    soup_prety = soup.prettify()
    try:
        file = open(sto_file_path, "w")
        file.write(str(soup_prety))

    except Exception as e:
        print(e)

def get_name():
    file = open(sto_file_path)
    soup = BeautifulSoup(file, "html.parser")
    real_name = soup.find("h1", "h2 mb-1 fw-bold").text.strip()
    return real_name

def get_image(start_url:str):
    file = open(sto_file_path)
    soup = BeautifulSoup(file, "html.parser")
    img_grob_gefunden = soup.find("div","d-md-none float-end text-end show-cover-mobile")
    img = img_grob_gefunden.find("img")
    img_url_intern = img.get('data-src')
    img_url = urljoin(start_url, img_url_intern)
    return img_url

def get_year() -> str:
    file = open(sto_file_path)
    soup = BeautifulSoup(file, "html.parser")
    jahr_start = soup.find("a", "small text-muted").text.strip()
    jahr_ende = soup.find("a", "small -textmuted").text.strip()
    jahr_zusammen= f"{jahr_start}-{jahr_ende}"
    return jahr_zusammen

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
        
        if ("/serie/" or "stream") not in href:
            continue
        found_urls.add(href)


        """
        absolute_url = urljoin(start_url, href)

        parsed = urlparse(absolute_url)
        if parsed.scheme in ("http", "https"):
            if "aniworld.to/anime/stream/" in absolute_url:
                absolute_url = absolute_url.replace("https://aniworld.to/anime/stream/", "")
                found_urls.add(absolute_url)
            elif "s.to/serie/" in absolute_url:
                absolute_url = absolute_url.replace("https://s.to/serie/", "")
                found_urls.add(absolute_url)
                """
        sorted_urls = sorted(found_urls)
    return sorted_urls

#get_sto_html()
#print(get_year())
#print(get_name())
#print(get_image(start_url))
#print(get_all_url_names(start_url))
