# Webscraper of autotrader using Selenium 

This project came about as my mum wanted to find a Citroen Berlingo to enjoy the festivals with this summer. My partner and I had recently written some [scripts](https://github.com/pmacg/cazooScraper) to scrape the Cazoo website in Python and I wrote a script to plot the cars in R using ggplot. More cars are on autotrader but this is a bit trickier to scrape as the autotrader website doesn't let you scrape it directly using a module in Python called "beautifulsoup", as it [thinks you are a bot](https://github.com/AmeliaES/cars/tree/f13d63fff0366a4ab55f93fc0c9050877eb5d4c3)! I found autotrader also has an [API](https://www.autotrader.co.uk/partners/retailer/auto-trader-connect) which would be more stable than scraping. But I doubt this is free to use! I then came across a great script and set of clear instructions here: https://www.shedloadofcode.com/blog/how-to-scrape-autotrader-with-python-and-selenium-to-search-for-multiple-makes-and-models

### Things I learnt from this project:
* web scraping using python, beautiful soup, selenium
* the debugging tool in PyCharm, conditional break points
* how to get other people's code to work
* how unstable webscraping can be
* how to use the dev tools on the chrome browser, especially to hover over elements. This helped when fixing the bug where the code was excluding private sellers and I could compare the html for private sellers and dealerships.
* explaining results to the client in non-jargon language

### TL;DR
[`scrapeAT.py`](scrapeAT.py) scrapes the autotrader website for Citroen Berlingos and writes to [`carsAT.csv`](carsAT.csv). Code is tweaked from https://github.com/shedloadofcode/autotrader-selenium-scraper/blob/main/autotrader-scraper.py

## Interpreting plot for the client (ie. my mum)
![carsAT.png](carsAT.png?raw=true)

**Each point is a car. The darker the colour the cheaper the car. Cars/points in the bottom right quadrant that are a dark colour (ie. cheaper) are probably worth looking at on autotrader. To find the URLs for these cars download the [carsAT.csv](carsAT.csv) and find the car from the year, mileage and price from the plot.**

### Prerequisites
* Install ChromeDriver to match version of chrome: https://googlechromelabs.github.io/chrome-for-testing/#stable

* This is version I installed:
https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/mac-x64/chromedriver-mac-x64.zip

* My version of Chrome is: Version 123.0.6312.87 (Official Build) (x86_64)

* Instructions on how to install ChromeDriver here:
https://www.swtestacademy.com/install-chrome-driver-on-mac/

### Data cleaning:
*Also written in: [`scrapeAT.py`](scrapeAT.py)*
* Removes duplicates (excluding the URL/link column). Some cars are duplicated because there are also adverts for the same car.
* Fixed bug of missing data for the year by changing regular expression for removing "reg" from the "year" field.

### Data plotting:
[`exploreCarsAT.py](exploreCars.py) creates the scatter plot above.
  
