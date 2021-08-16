import json
from abc import abstractmethod, ABC

import pandas as pd

from src.models import CountryData


class AbstractOutputGenerator(ABC):

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def generate(self):
        raise NotImplementedError


class ConsoleTimeResume(AbstractOutputGenerator):
    """Print some useful times in console."""

    def generate(self):
        df = pd.DataFrame(self.data)
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


class JSONResult(AbstractOutputGenerator):
    """Store results in JSON file in out/data.json path."""

    def generate(self):
        with open('out/data.json', 'w') as file:
            json.dump(self.data, file, indent=2, ensure_ascii=False)


class SQLiteResult(AbstractOutputGenerator):
    """Store results in sqlite db in countrydata table."""

    def generate(self):
        rows_to_create = [CountryData(**row) for row in self.data]
        CountryData.bulk_create(rows_to_create)


# Note that we can also upload the data other sources
# There are some examples bellow:


class S3Result(AbstractOutputGenerator):
    def generate(self):
        pass


class PostgreSQLResult(AbstractOutputGenerator):
    def generate(self):
        pass
