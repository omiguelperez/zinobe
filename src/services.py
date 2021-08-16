import json
import os

import pandas as pd

from src.encoding import encode_to_sha1
from src.decorators import add_execution_time
from src.models import save_countrydata_rows


class CountriesETL:
    """
    Download countries and regions data from third-party services such as
    rapidapi and restcountries, process it and save in custom formats according
    to business rules.
    """

    def __init__(self, regions_service, countries_service):
        self._regions = regions_service
        self._countries = countries_service

    @add_execution_time
    def generate_processed_country_data(self, region_name):
        country = self._countries.get_first_by_region(region_name)
        encrypted_lang = encode_to_sha1(country['language'])
        row_data = {
            'country_name': country['name'],
            'city_name': country['capital'],
            'language': encrypted_lang,
        }
        return row_data

    def print_time_resume(self, rows):
        df = pd.DataFrame(rows)
        try:
            total_time = df["time"].sum()
            avrg_time = df["time"].mean()
            min_time = df["time"].min()
            max_time = df["time"].max()

            print(f'total time: {total_time}')
            print(f'average time: {avrg_time}')
            print(f'min time: {min_time}')
            print(f'max time: {max_time}')
        except KeyError:
            return "Invalid columns, check rows list."

    def save_rows(self, rows):
        with open('out/data.json', 'w') as file:
            json.dump(rows, file, indent=2, ensure_ascii=False)

        save_countrydata_rows(rows)

    def execute(self):
        # Extract and process
        regions = self._regions.extract_names()
        rows = [
            self.generate_processed_country_data(region)
            for region in regions
        ]

        # Load data to several output sources
        self.print_time_resume(rows)
        self.save_rows(rows)