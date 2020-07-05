import os
import logging
import connexion
from logging.handlers import RotatingFileHandler
from peewee_migrate.router import Router, load_models
from peewee_migrate.auto import diff_many
import pavlov_central.storage
import pavlov_central.storage.models
from pavlov_central.storage.models.base_model import ext_db
from pavlov_central.api import encoder


def start_api():
    app = connexion.App(__name__, specification_dir='./api/openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Pavlov Central API'},
                pythonic_params=True)
    app.run(port=5000)


def init_logging():
    r_handler = RotatingFileHandler(
        filename='/tmp/pavlov_central.log', maxBytes=1000000, backupCount=3
    )
    r_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(threadName)s %(funcName)s: %(message)s"))
    logging.getLogger().addHandler(r_handler)
    logging.getLogger().setLevel(logging.DEBUG)


def run_db_migration(database):
    db_storage_dir = os.path.dirname(pavlov_central.storage.__file__)
    db_migrations_dir = os.path.join(db_storage_dir, 'migrations')

    router = Router(
        database,
        migrate_dir=db_migrations_dir,
        migrate_table='migration',
        logger=logging.getLogger(),
        ignore=['basemodel', 'basedatamodel']
    )
    print('Run migrations..')

    router.run()

    # check migrations
    src_models = load_models(pavlov_central.storage.models)
    if router.ignore:
        src_models = [m for m in src_models if m.get_table_name() not in router.ignore]

    db_models = router.migrator.orm.values()

    diff_found = diff_many(src_models, db_models, router.migrator, reverse=False)

    if len(diff_found) > 0:
        logging.warning('migrations diff_found={}'.format(diff_found))
        print('migrations diff_found={}'.format(diff_found))
        raise RuntimeError('Check db migrations is failed')


if __name__ == '__main__':
    init_logging()
    run_db_migration(ext_db)
    start_api()
