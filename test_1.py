from requests import request
from bs4 import BeautifulSoup
import requests


serien_url= "https://aniworld.to/anime/stream/07-ghost"
file_name= "seite.html"


def load_test_site(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(serien_url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    seite = open(file_name, "w")
    seite.write(soup.prettify())

def get_year(file_name):
    f = open(file_name)
    soup = BeautifulSoup(f,features="html.parser")
    jahr_start = soup.find("span", itemprop="startDate").find("a").text.strip()
    jahr_ende = soup.find("span", itemprop="startDate").find("a").text.strip()
    jahr_zusammen= f"{jahr_start}-{jahr_ende}"
    print(jahr_zusammen)

def get_name(file_name):
    f = open(file_name)
    soup = BeautifulSoup(f,features="html.parser")
    real_name = soup.find("h1").find("span").text.strip()
    print(real_name)

get_year(file_name)
get_name(file_name)