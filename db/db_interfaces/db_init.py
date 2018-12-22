import yaml
import cassandra
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection, management
try:
    from .object_mappers import class_list
except Exception:
    from object_mappers import class_list
from importlib import import_module


DB_CONFIG_NAME = "config.yml"


def read_config():
    config = open(DB_CONFIG_NAME, 'r')
    cfg = yaml.load(config)
    return cfg


def connect_to_db(connection):
    cluster = Cluster(contact_points=connection["address"],
                      port=connection["port"])
    try:
        session = cluster.connect()
    except Exception as e:
        print(e)
        exit(1)
    session.default_timeout = 60
    if __name__ == "__main__":
        session.execute("ALTER KEYSPACE system_auth WITH replication = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };")
    return session


def create_keyspace(session, keyspace):
    connection.set_session(session)
    try:
        management.create_keyspace_simple(keyspace["name"],
                                          replication_factor=keyspace["factor"])
    except cassandra.AlreadyExists:
        pass
    session.set_keyspace(keyspace["name"])
    connection.set_session(session)
    return session


def create_table():
    for i in class_list:
        try:
            _module = import_module(".object_mappers", package="db_interfaces")
            _class = getattr(_module, i)
        except Exception:
            _module = import_module("object_mappers", package="db_interfaces")
            _class = getattr(_module, i)
        try:
            management.sync_table(_class)
        except cassandra.AlreadyExists:
            pass
        except cassandra.protocol.ServerError as e:
            print(e)
            pass


def init_db():
    db_params = read_config()
    session = connect_to_db(db_params["db"]["connection"])
    session = create_keyspace(session, db_params["db"]["keyspace"])
    create_table()
    return session


if __name__ == '__main__':
    init_db()
