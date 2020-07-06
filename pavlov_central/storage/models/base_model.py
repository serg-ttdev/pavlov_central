import peewee as pw
from playhouse.postgres_ext import *

DB = PostgresqlExtDatabase('central', user='pavlov', host='localhost', port=5432)


class BaseModel(pw.Model):
    class Meta:
        database = DB

    @classmethod
    def get_database(cls):
        return cls._meta.database

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name
