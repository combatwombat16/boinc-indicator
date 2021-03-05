import queue
from threading import Event

# Shared queue
workQueue = queue.Queue(5000)

# Boinc servers to connect to
boinc_hosts = [
    "192.168.1.220", "192.168.1.221", "192.168.1.222"
    , "192.168.1.223", "192.168.1.224", "192.168.1.225"
    , "192.168.1.230", "192.168.1.231"
    , "192.168.1.240", "192.168.1.241"
]
# Thread variables for Boinc connections
producer_threads = list()
producerStopEvent = Event()

# InfluxDB server info
influxdb_hosts = ["192.168.1.230"]
influxdb_database = 'boinc_test'
# Thread variables for Boinc connections
consumer_threads = list()
consumerStopEvent = Event()
