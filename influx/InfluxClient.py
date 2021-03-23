from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxClient(object):
    def __init__(self, token, org, host, port=8086):
        self.token = token
        self.org = org
        self.host = host
        self.port = port

    def write_data(self, data: [Point], bucket):
        client = InfluxDBClient(url="http://%s:%s" % (self.host, self.port)
                                , token=self.token
                                , org=self.org
                                , timeout=1000)
        _write_client = client.write_api(write_options=SYNCHRONOUS)
        _write_client.write(bucket=bucket
                            , org=self.org
                            , record=data)
        _write_client.close()
        client.close()
