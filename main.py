# This is a sample Python script.
import requests
from bs4 import BeautifulSoup

class CazooCar(object):
    """
    A class representing a car for sale on the cazoo website.
    """

    def __init__(self, bs_cazoo_table_element):
        """
        Initialise the object from a beautiful soup table element.
        :param bs_cazoo_table_element:
        """
        make_model = bs_cazoo_table_element.find(
            attrs={'class': 'vehicle-cardstyles__CustomTitle-sc-1bxv5iu-9 IEXri'}).text
        self.make = make_model.split()[0]
        self.model = make_model.split()[1].strip()

        version = bs_cazoo_table_element.find(
            attrs={'class': 'vehicle-cardstyles__DisplayVariant-sc-1bxv5iu-10 dwOxWL'}).text
        version = version.split()
        self.engine = ''.join(version[0])
        self.trim = " ".join(version[1:])

        self.price = bs_cazoo_table_element.find(
            attrs={'data-test-id': 'card-pricing-full-price-gb'}).text
        self.price = self.price.split('£')[-1].replace(',', '')

        # Get the tags. They always seem to be:
        #  miles
        #  year
        #  transmission
        #  fuel
        tags = bs_cazoo_table_element.find(
            attrs={'data-test-id': 'tags'}).find_all('span')
        self.mileage = tags[0].text.split()[0].replace(',', '')
        self.year = tags[1].text.split()[0]
        self.transmission = tags[2].text
        self.fuel = tags[3].text

        self.link = "www.cazoo.co.uk" + bs_cazoo_table_element.find('a')['href']


def get_cars_from_url(url):
    print(f"Processing url: {url}...")
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    pageselection = soup.find(attrs={'aria-label': 'Pagination'})
    numpages = 1
    if pageselection != None:
        pages = pageselection.find_all(attrs={'class': 'cui__sc-j9mjm2-0 cui__sc-j9mjm2-3 jkCaUj dUXlEO'})
        numpages = int(pages[-1].text.split()[-1])

    for page in range(1, numpages + 1):
        print(f"Processing page {page}/{numpages}...")
        if pageselection != None:
            new_url = url + '?page=' + str(page)
            res = requests.get(new_url)
            soup = BeautifulSoup(res.content, 'html.parser')
        table = soup.find(attrs={'class': "resultsstyles__ResultsList-sc-11kjmxu-0 ezjHRs"})
        if table != None:
            cars = table.find_all('li', attrs={'class': 'resultsstyles__ResultsListItem-sc-11kjmxu-1'})
            for car in cars[1:]:
                yield CazooCar(car)
        else:
            print(f"No car found for {url}")


def main():
    urls = [
        'https://www.cazoo.co.uk/cars/vauxhall/corsa/',
        'https://www.cazoo.co.uk/cars/volkswagen/golf/',
        'https://www.cazoo.co.uk/cars/volkswagen/polo/',
        'https://www.cazoo.co.uk/cars/toyota/corolla/',
        'https://www.cazoo.co.uk/cars/renault/clio/',
        'https://www.cazoo.co.uk/cars/toyota/yaris/',
        'https://www.cazoo.co.uk/cars/honda/jazz/',
        'https://www.cazoo.co.uk/cars/ford/fiesta/',
        'https://www.cazoo.co.uk/cars/kia/picanto/',
        'https://www.cazoo.co.uk/cars/peugeot/208/',
        'https://www.cazoo.co.uk/cars/hyundai/i10/',
        'https://www.cazoo.co.uk/cars/seat/ibiza/',
        'https://www.cazoo.co.uk/cars/audi/a1/',
        'https://www.cazoo.co.uk/cars/skoda/fabia',
        'https://www.cazoo.co.uk/cars/dacia/sandero'
        ]

    number_of_cars = 0
    with open("cars.csv", 'w') as fout:
        fout.write("make,model,engine,trim,mileage,year,transmission,fuel,price,url\n")

        for url in urls:
            for car in get_cars_from_url(url):
                number_of_cars += 1
                fout.write(f"{car.make},{car.model},{car.engine},{car.trim},")
                fout.write(f"{car.mileage},{car.year},{car.transmission},")
                fout.write(f"{car.fuel},{car.price},{car.link}\n")

    print(f"Found {number_of_cars} cars.")


if __name__ == "__main__":
    main()

