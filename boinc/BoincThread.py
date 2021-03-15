import logging
from threading import Thread, Event
from queue import Queue

from boinc.BoincClient import BoincClient


class BoincThread(Thread):
    def __init__(self, event: Event, shared_queue: Queue, ip, name, bucket, passwd='boinc', daemon=True):
        Thread.__init__(self, daemon=daemon)
        self.ip = ip
        self.name = name
        self.passwd = passwd
        self.queue = shared_queue
        self.stopped = event
        self.bucket = bucket
        logging.info('Creating BoincClient to host %s' % (self.ip))
        self.client = BoincClient(host=self.ip, passwd=self.passwd)  # .__enter__()

    def __exit__(self, *args):
        logging.info('Disconnecting from Boinc host at %s' % (self.ip))
        self.client.__exit__()

    def run(self):
        while not self.stopped.wait(5):
            with self.client:
                for point in self.client.getInfluxPoints(bucket=self.bucket):
                    self.queue.put(point)
            logging.debug('Added points host %s, queue size now %d' % (self.ip, self.queue.qsize()))
        self.__exit__()
