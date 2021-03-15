import logging
from threading import Thread, Event
from queue import Queue

from gridcoin.GridcoinClient import GridcoinClient


class GridcoinThread(Thread):
    def __init__(self, event: Event, shared_queue: Queue, ip, port, user, passwd, name, bucket, daemon=True):
        Thread.__init__(self, daemon=daemon)
        self.name = name
        self.stopped = event
        self.queue = shared_queue
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.bucket = bucket
        logging.info("Connecting to %s on port %s" % (self.ip, self.port))
        self.client = GridcoinClient(ip=self.ip, port=self.port, user=self.user, passwd=self.passwd)

    def run(self):
        while not self.stopped.wait(10):
            for point in self.client.getGRCPoints(bucket=self.bucket):
                self.queue.put(point, block=True, timeout=.3)
            logging.debug('Added points host %s, queue size now %d' % (self.ip, self.queue.qsize()))