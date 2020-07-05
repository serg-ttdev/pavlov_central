import connexion
from connexion import NoContent
from pavlov_central.api.helper.api_helper import merge_dict
from pavlov_central.storage.models.server import Server


def handle_get_server_list():
    return Server.select().dicts[:]


def handle_get_server(server_name):
    server = Server.get_server(server_name)
    if server is None:
        return 'Server not found', 404
    else:
        return server.serialize


def handle_add_server(server_props):
    server_name = server_props.get('name')
    server = Server.get_server(server_name)
    if server is not None:
        return 'Server already exists', 409
    else:
        return Server.add_server(server_props)


def handle_update_server(server_name):
    if not connexion.request.is_json:
        return 'Request body empty or not valid json', 400
    server_update = connexion.request.get_json()
    server = Server.get_server(server_name)
    if server is None:
        return f'Server {server_name} not found', 404
    if server_name != server_update.get('name'):
        return 'Server name must be the same in the query and in the request body', 400

    new_server_params = merge_dict(server, server_update)
    if Server.update_server(new_server_params):
        return NoContent, 204


def handle_delete_server(server_name):
    server = Server.get_server(server_name)
    if Server.delete_server(server_name):
        return NoContent, 204
    else:
        return 'Sensor not found', 404
