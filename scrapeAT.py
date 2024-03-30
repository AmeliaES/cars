import requests
from bs4 import BeautifulSoup

URL = "https://www.autotrader.co.uk/car-search?make=Citroen&model=Berlingo&postcode=E17BT"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")


with open("test.html", "w") as output:
    output.write(str(soup))


