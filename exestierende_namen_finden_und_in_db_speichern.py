from bs4 import BeautifulSoup
import requests

def prüfe_ob_url_existiert(url):
    r = requests.get(f"https://aniworld.to/anime/stream/{url}")
    if not r.status_code == 200:
        return
    
    soup = BeautifulSoup(r.text, "html.parser")

    # Finde das span innerhalb der Serie-Titel-Struktur
    title_div = soup.find("div", class_="series-title")
    if not title_div:
        return

    if title_div:
        span = title_div.find("span")
        if span:
            name = span.get_text(strip=True)
            print(f"In der {durchsuchte_urls} gesuchten URL die Serie {name} gefunden mit der url {url}")
