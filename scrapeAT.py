# type: ignore

"""
Enables the automation of searching for multiple makes/models on Autotrader UK using Selenium and Regex.

Set your criteria and cars makes/models.

Data is then output to an Excel file in the same directory.

Running Chrome Version 119.0.6045.106 and using Stable Win64 ChromeDriver from:
https://googlechromelabs.github.io/chrome-for-testing/
https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/119.0.6045.105/win64/chromedriver-win64.zip
"""
import os
import re
import time
import datetime

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

criteria = {
    "postcode": "E1 6AN"
    # "radius": "20",
    # "year_from": "2010",
    # "year_to": "2014",
    # "price_from": "3000",
    # "price_to": "6500",
}

cars = [
    {
        "make": "Citroen",
        "model": "Berlingo"
    }
]


def scrape_autotrader(cars, criteria):
    chrome_options = Options()
    chrome_options.add_argument("_tt_enable_cookie=1")
    driver = webdriver.Chrome()
    data = []

    for car in cars:

        url = "https://www.autotrader.co.uk/motorhome-search?" + \
              f"make={car['make']}&" + \
              f"model={car['model']}&" + \
              f"postcode={criteria['postcode']}&"
              # f"radius={criteria['radius']}&" + \
              # "sort=relevance&" + \
              # f"year-from={criteria['year_from']}&" + \
              # f"year-to={criteria['year_to']}&" + \
              # f"price-from={criteria['price_from']}&" + \
              # f"price-to={criteria['price_to']}"

        driver.get(url)

        print(f"Searching for {car['make']} {car['model']}...")

        time.sleep(5)

        source = driver.page_source
        content = BeautifulSoup(source, "html.parser")

        try:
            number_of_pages = int(content.find("p", text=re.compile(r'Page \d{1,2} of \d{1,2}')).text.split()[-1])
        except:
            print("No results found.")
            continue

        print(f"There are {number_of_pages} pages in total.")

        for i in range(int(number_of_pages)):
            driver.get(url + f"&page={str(i + 1)}")

            time.sleep(5)
            page_source = driver.page_source
            content = BeautifulSoup(page_source, "html.parser")

            articles = []

            # Assuming content is your BeautifulSoup object
            private_seller_listings = content.findAll("section", attrs={"data-testid": "private-seller-listing"})
            trader_seller_listings = content.findAll("section", attrs={"data-testid": "trader-seller-listing"})

            articles.extend(private_seller_listings)
            articles.extend(trader_seller_listings)

            print(f"Scraping page {str(i + 1)}...")

            for article in articles:
                details = {
                    "name": car['make'] + " " + car['model'],
                    "price": re.search("[£]\d+(\,\d{3})?", article.text).group(0),
                    "year": None,
                    "mileage": None,
                    "transmission": None,
                    "fuel": None,
                    "engine": None,
                    "owners": None,
                    "location": None,
                    "distance": None,
                    "link": article.find("a", {"href": re.compile(r'/motorhome-details/')}).get("href")
                }

                try:
                    seller_info = article.find("p", attrs={"data-testid": "search-listing-seller"}).text
                    location = seller_info.split("Dealer location")[1]
                    details["location"] = location.split("(")[0]
                    details["distance"] = location.split("(")[1].replace(" mile)", "").replace(" miles)", "")
                except:
                    print("Seller information not found.")

                specs_list = article.find("ul", attrs={"data-testid": "search-listing-specs"})
                for i, spec in enumerate(specs_list):
                    if i == 0:
                        details["year"] = spec.text

                    if "miles" in spec.text:
                        details["mileage"] = spec.text

                    if spec.text in ["Manual", "Automatic"]:
                        details["transmission"] = spec.text

                    if "." in spec.text and "L" in spec.text:
                        details["engine"] = spec.text

                    if spec.text in ["Petrol", "Diesel"]:
                        details["fuel"] = spec.text

                    if "owner" in spec.text:
                        details["owners"] = spec.text.split()[0]

                data.append(details)

            print(f"Page {str(i + 1)} scraped. ({len(articles)} articles)")
            time.sleep(5)

        print("\n\n")

    print(f"{len(data)} cars total found.")

    return data


def output_data_to_csv(data, criteria):
    df = pd.DataFrame(data)

    df["price"] = df["price"].str.replace("£", "").str.replace(",", "")
    df["price"] = pd.to_numeric(df["price"], errors="coerce").astype("Int64")

    df["year"] = df["year"].str.replace(r"\s(\([a-zA-Z0-9]* reg\))", "", regex=True)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    df["mileage"] = df["mileage"].str.replace(",", "").str.replace(" miles", "")
    df["mileage"] = pd.to_numeric(df["mileage"], errors="coerce").astype("Int64")

    now = datetime.datetime.now()
    df["miles_pa"] = df["mileage"] / (now.year - df["year"])
    df["miles_pa"].fillna(0, inplace=True)
    df["miles_pa"] = df["miles_pa"].astype(int)

    df["owners"] = df["owners"].fillna("-1")
    df["owners"] = df["owners"].astype(int)

    df["distance"] = df["distance"].fillna("-1")
    df["distance"] = df["distance"].astype(int)

    df["link"] = "https://www.autotrader.co.uk" + df["link"]

    df = df[[
        "name",
        "link",
        "price",
        "year",
        "mileage",
        "miles_pa",
        "owners",
        "distance",
        "location",
        "engine",
        "transmission",
        "fuel",
    ]]

    # df = df[df["price"] < int(criteria["price_to"])]

    df = df.sort_values(by="price", ascending=True)

    # Drop dupliacted cars which show more than once if there's an advert
    df = df.drop_duplicates(subset=df.columns.difference(['link']))

    df.to_csv('carsAT.csv', index = False)

    print(f"{len(df)} cars total saved.")

    print("Output saved to current directory as 'carsAT.csv'.")


if __name__ == "__main__":
    data = scrape_autotrader(cars, criteria)
    output_data_to_csv(data, criteria)
