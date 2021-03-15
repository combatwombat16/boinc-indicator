from influxdb_client import InfluxDBClient, WriteOptions, Point


class InfluxClient(object):
    def __init__(self, token, org, host, port=8086):
        self.token = token
        self.org = org
        self.host = host
        self.port = port
        self._client = InfluxDBClient(url="http://%s:%s" % (self.host, self.port)
                                      , token=self.token
                                      , org=self.org)
        self.write_options = WriteOptions(batch_size=250, flush_interval=1000, jitter_interval=50)
        self._write_client = self._client.write_api(write_options=self.write_options)

    def __exit__(self, *args):
        self._write_client.close()
        self._client.close()

    def write_data(self, data: [Point], bucket):
        self._write_client.write(bucket=bucket
                                 , org=self.org
                                 , record=data)
        #self._write_client.close()
