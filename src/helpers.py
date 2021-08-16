import os

import requests


class RapidAPIClient:

    def __init__(self):
        self._api_key = os.environ.get('RAPIDAPI_API_KEY')

    def extract_names(self):
        url = "https://restcountries-v1.p.rapidapi.com/all"

        headers = {
            'x-rapidapi-key': self._api_key,
            'x-rapidapi-host': "restcountries-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)
        return {
            country['region']
            for country in response.json()
            if country['region'] != ''
        }


class RESTCountriesClient:

    def get_first_by_region(self, region):
        url = f'https://restcountries.eu/rest/v2/region/{region}'

        response = requests.request("GET", url)
        country_data = response.json()[0]
        return {
            'name': country_data['name'],
            'capital': country_data['capital'],
            'language': country_data['languages'][0]['name'],
        }
