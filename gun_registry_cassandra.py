from gun_registry import GunRegistry

from cassandra.cqlengine import connection, columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table, create_keyspace_simple


class Record(Model):
    key = columns.Bytes(primary_key=True)
    enc_values = columns.List(columns.Blob())


class GunRegistryCassandra(GunRegistry):
    def __init__(self, hosts, keyspace='gunregistry',
                 replication_factor=1, **cqlengine_params):
        self.keyspace = keyspace
        connection.setup(hosts, keyspace, **cqlengine_params)
        create_keyspace_simple(keyspace, replication_factor)
        sync_table(Record)

    def _get_records(self, key):
        record = Record.objects(key=key).get()
        return record['enc_values']

    def _add_record(self, key, value):
        Record.objects(key=key).update(enc_values__append=[value])
