from datetime import datetime

from peewee import Model, SqliteDatabase, CharField, FloatField, DateTimeField

db = SqliteDatabase('out/db.sqlite3')


class CountryData(Model):
    country_name = CharField()
    city_name = CharField()
    language = CharField()
    time = FloatField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
