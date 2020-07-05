import peewee as pw
from playhouse.postgres_ext import *

ext_db = PostgresqlExtDatabase('pavlov_central', user='pavlov')


class BaseModel(pw.Model):
    class Meta:
        database = ext_db

    @classmethod
    def get_database(cls):
        return cls._meta.database

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name
