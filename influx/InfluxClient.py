from influxdb import InfluxDBClient


class InfluxClient(object):
    def __init__(self, database, host, port=8086):
        self.database = database
        self.host = host
        self.port = port
        self.client = InfluxDBClient(host=self.host, port=self.port, pool_size=3)

    def __enter__(self):
        databases = self.client.get_list_database()
        if len([db["name"] for db in databases if self.database == db["name"]]) == 0:
            print("Did not find database %s in influx host %s" % (self.database, self.host))
            self.client.create_database(self.database)
            self.client.switch_database(self.database)
        else:
            print("Found database %s in influx host %s" % (self.database, self.host))
            self.client.switch_database(self.database)
        return self

    def __exit__(self, *args):
        self.client.close()

    def write_data(self, data):
        self.client.write_points(points=data, database=self.database, batch_size=250)
