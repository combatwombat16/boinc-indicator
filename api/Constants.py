import queue
from threading import Event


class Constants(object):
    work_queue = queue.Queue(5000)

    # Producer components
    # Boinc servers to connect to
    boinc_hosts = [
        "192.168.1.220", "192.168.1.221", "192.168.1.222"
        , "192.168.1.223", "192.168.1.224", "192.168.1.225"
        , "192.168.1.230", "192.168.1.231"
        , "192.168.1.240", "192.168.1.241"
    ]
    # Thread variables for Boinc connections
    boinc_producer_threads = list()
    boinc_producer_stop_event = Event()
    # Gridcoin servers to connect to
    gridcoin_hosts = ["192.168.1.231"]
    gridcoin_port = "7216"
    gridcoin_user = "gridcoinrpc"
    gridcoin_pass = "gridcoin"
    # Thread variables for Gridcoin connections
    gridcoin_producer_threads = list()
    gridcoin_producer_stop_event = Event()

    # Consumer components
    # InfluxDB server info
    influxdb_hosts = ["192.168.1.210"]
    influxdb_org = "PandaInc"
    influxdb_token = "sDojBrldZNcacZv7xZD9DSukIS2vIOsnc5lGCsHmohFstY2GpRrTNmRESEK3tiGLgAGcBtSYnqxtq5LskdFiAA=="
    influxdb_boinc_bucket = "panda-boinc"
    influxdb_grc_bucket = "panda-coin"
    # Thread variables for influxdb connections
    influxdb_consumer_threads = list()
    influxdb_consumer_stop_event = Event()
