import queue
from threading import Event, Lock

boinc_lock = Lock()
gridcoin_lock = Lock()

# Producer components
# Boinc servers to connect to
boinc_work_queue = queue.Queue(5000)
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
gridcoin_work_queue = queue.Queue(1000)
gridcoin_hosts = ["192.168.1.231"]
gridcoin_port = "7216"
gridcoin_user = "gridcoinrpc"
gridcoin_pass = "gridcoin"
# Thread variables for Gridcoin connections
gridcoin_producer_threads = list()
gridcoin_producer_stop_event = Event()

# Consumer components
# InfluxDB server info
influxdb_hosts = ["192.168.1.230"]
influxdb_boinc_database = "boinc"
influxdb_grc_database = "gridcoin"
# Thread variables for Boinc connections
boinc_consumer_threads = list()
boinc_consumer_stop_event = Event()
# Thread variables for Gridcoin connections
gridcoin_consumer_threads = list()
gridcoin_consumer_stop_event = Event()
