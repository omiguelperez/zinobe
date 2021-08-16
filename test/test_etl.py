import json

import httpretty

from src.encoding import encode_to_sha1
from src.etls import CountriesETL
from src.helpers import RapidAPIClient, RESTCountriesClient
from src.output_generators import AbstractOutputGenerator


class FakeOutputGenerator(AbstractOutputGenerator):

    gen_data = None

    def generate(self):
        FakeOutputGenerator.gen_data = self.data


@httpretty.activate
def test_download_countries_data():
    httpretty.register_uri(
        httpretty.GET,
        "https://restcountries-v1.p.rapidapi.com/all",
        body=json.dumps([
            {
                'region': 'Europe',
            },
        ])
    )

    httpretty.register_uri(
        httpretty.GET,
        "https://restcountries.eu/rest/v2/region/Europe",
        body=json.dumps([
            {
                'name': 'Albania',
                'capital': 'Tirana',
                'languages': [
                    {
                        "iso639_1": "sq",
                        "iso639_2": "sqi",
                        "name": "Albanian",
                        "nativeName": "Shqip"
                    }
                ]
            }
        ])
    )

    fake_generator = FakeOutputGenerator
    etl = CountriesETL(
        outputs=[
            fake_generator,
        ],
        # Custom ETL helpers
        regions_service=RapidAPIClient(),
        countries_service=RESTCountriesClient(),
    )

    etl.execute()

    assert fake_generator.gen_data is not None
    gen_data = fake_generator.gen_data[0]
    gen_data.pop('time')

    expected_data = {
        'country_name': 'Albania',
        'city_name': 'Tirana',
        'language': encode_to_sha1('Albanian'),
    }
    assert gen_data == expected_data
