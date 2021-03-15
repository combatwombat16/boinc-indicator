from threading import Thread, Event
import logging
from queue import Queue
from requests.sessions import Session

from influx.InfluxClient import InfluxClient


class InfluxThread(Thread):
    def __init__(self, name, event: Event, shared_queue: Queue, org, token, db_host, port=8086, daemon=True):
        Thread.__init__(self, daemon=daemon)
        self.queue = shared_queue
        self.db_host = db_host
        self.name = name
        self.port = port
        self.stopped = event
        self.org = org
        self.token = token
        logging.info('Connecting to InfluxDB at host %s' % (self.db_host))
        self.collector = InfluxClient(host=self.db_host
                                      , port=self.port
                                      , org=self.org
                                      , token=self.token)

    def __exit__(self):
        logging.debug("Draining pool one last time then exiting")
        data = dict()
        while not self.queue.empty():
            rec = self.queue.get()
            if rec["bucket"] not in data.keys():
                data[rec["bucket"]] = [rec["point"]]
            else:
                data[rec["bucket"]].append(rec["point"])
        for bucket in data:
            self.collector.write_data(data=data[bucket], bucket=bucket)
        logging.info("Disconnecting from Influx host")
        self.collector.__exit__()

    def run(self):
        data = dict()
        while not self.stopped.wait(10):
            logging.debug('Draining %d points from the queue' % (self.queue.qsize()))
            while not self.queue.empty():
                rec = self.queue.get(block=True, timeout=1)
                if rec["bucket"] not in data.keys():
                    data[rec["bucket"]] = [rec["point"]]
                else:
                    data[rec["bucket"]].append(rec["point"])
            for bucket in data:
                self.collector.write_data(data=data[bucket], bucket=bucket)
        self.__exit__()
