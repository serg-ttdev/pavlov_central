import os
import peewee as pw
from playhouse.sqlite_ext import SqliteExtDatabase

DB = SqliteExtDatabase(
    os.path.expanduser('~/tmp/pavlov.db'),
    pragmas=(
        ('journal_mode', 'wal'),     # Use WAL-mode
    )
)


class BaseModel(pw.Model):
    class Meta:
        database = DB

    @classmethod
    def get_database(cls):
        return cls._meta.database

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name
