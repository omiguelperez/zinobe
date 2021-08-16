import json
import time
from hashlib import sha1
import pandas as pd
import requests

from db import save_countrydata_rows


class RapidAPIClient:

    def __init__(self, api_key):
        self._api_key = api_key

    def list_regions(self):
        url = "https://restcountries-v1.p.rapidapi.com/all"

        headers = {
            'x-rapidapi-key': "xxxx",
            'x-rapidapi-host': "restcountries-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)
        return {
            country['region']
            for country in response.json()
            if country['region'] != ''
        }


class RESTCountriesClient:

    def get_first_country_by_region(self, region):
        url = f'https://restcountries.eu/rest/v2/region/{region}'

        response = requests.request("GET", url)
        return response.json()[0]


class Zinobe:

    def encode_language_to_sha1(self, lang: str):
        if type(lang) != str:
            raise TypeError('Invalid language. Must be a string.')
        return sha1(lang.encode('utf-8')).hexdigest()

    def generate_row(self, region):
        restcountries = RESTCountriesClient()
        begin = time.time()
        country = restcountries.get_first_country_by_region(region)
        encrypted_lang = self.encode_language_to_sha1(country['languages'][0]['name'])
        end = time.time()
        elapsed_time = end - begin
        row_data = {
            'country_name': country['name'],
            'city_name': country['capital'],
            'language': encrypted_lang,
            'time': elapsed_time,
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
        with open('data.json', 'w') as file:
            json.dump(rows, file, indent=2, ensure_ascii=False)

        save_countrydata_rows(rows)

    def generate_output_data(self):
        rapidapi = RapidAPIClient(api_key='')

        regions = rapidapi.list_regions()
        rows = [
            self.generate_row(region)
            for region in regions
        ]
        self.print_time_resume(rows)
        self.save_rows(rows)


if __name__ == '__main__':
    zinobe = Zinobe()
    zinobe.generate_output_data()
