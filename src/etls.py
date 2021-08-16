from abc import abstractmethod, ABC
from typing import List

from src.encoding import encode_to_sha1
from src.decorators import add_execution_time


class AbstractETL(ABC):

    def __init__(self, outputs: List, *args, **kwargs):
        self._outputs = outputs

    def load(self, data):
        # Load data to several output sources
        for output_class in self._outputs:
            output = output_class(data=data)
            output.generate()


class CountriesETL(AbstractETL):
    """
    Download countries and regions data from third-party services such as
    rapidapi and restcountries, process it and save in custom formats according
    to business rules.
    """

    def __init__(self, outputs, regions_service, countries_service):
        super().__init__(outputs)

        # Custom ETL services
        self._regions = regions_service
        self._countries = countries_service

    @add_execution_time
    def generate_row(self, region_name):
        """Build object with country data such as Capital and Encoded Language."""
        country = self._countries.get_first_by_region(region_name)
        if not country:
            raise Exception(f'No countries found for region: {region_name}')

        encrypted_lang = encode_to_sha1(country['language'])
        row_data = {
            'country_name': country['name'],
            'city_name': country['capital'],
            'language': encrypted_lang,
        }
        return row_data

    def execute(self):
        # Extract and process
        regions = self._regions.extract_names()
        rows = [self.generate_row(region) for region in regions]

        self.load(data=rows)
