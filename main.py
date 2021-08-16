from src.output_generators import ConsoleTimeResume, JSONResult, SQLiteResult
from src.etls import CountriesETL
from src.helpers import RapidAPIClient, RESTCountriesClient
from src.models import db, CountryData

if __name__ == '__main__':

    # Setup
    db.connect()
    db.create_tables([
        CountryData,
    ])

    # Run process
    etl = CountriesETL(
        outputs=[
            ConsoleTimeResume,
            JSONResult,
            SQLiteResult,
        ],
        # Custom ETL helpers
        regions_service=RapidAPIClient(),
        countries_service=RESTCountriesClient(),
    )
    etl.execute()
