from src.services import CountriesETL
from src.helpers import RapidAPIClient, RESTCountriesClient

if __name__ == '__main__':
    etl = CountriesETL(
        regions_service=RapidAPIClient(),
        countries_service=RESTCountriesClient(),
    )
    etl.execute()
