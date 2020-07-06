import peewee as pw
from peewee import DoesNotExist
from pavlov_central.storage.models.base_model import BaseModel


class Server(BaseModel):
    name = pw.TextField(primary_key=True)
    ip = pw.IPField()

    class Meta:
        table_name = 'server'

    @property
    def serialize(self):
        data = {
            'name': self.name,
            'ip': self.ip
        }
        return data

    @classmethod
    def get_server(cls, server_name):
        try:
            server = (
                Server
                .select()
                .where(Server.name == server_name)
                .get()
            )
            return server.serialize
        except DoesNotExist:
            return None

    @classmethod
    def add_server(cls, server_props):
        Server.insert(server_props).execute()
        return server_props

    @classmethod
    def update_server(cls, server_update):
        server_name = server_update.get('name')
        try:
            (
                Server
                .update(
                    ip=server_update.get('ip')
                )
                .where(Server.name == server_name)
                .execute()
            )
            return True
        except DoesNotExist:
            return False

    @classmethod
    def delete_server(cls, server_name):
        try:
            (
                Server
                .delete()
                .where(Server.name == server_name)
                .execute()
            )
            return True
        except DoesNotExist:
            return False