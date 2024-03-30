from autotrader_scraper import get_cars, save_csv, save_json
results = get_cars(
        make = "Audi",
        model = "A5",
        postcode = "SW1A 0AA",
        radius = 1500,
        min_year = 2005,
        max_year = 2020,
        include_writeoff = "include",
        max_attempts_per_page = 5,
        verbose = False
    )

print(results)