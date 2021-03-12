import logging
from threading import Thread, Event, Lock
from queue import Queue

from gridcoin.GridcoinClient import GridcoinClient


class GridcoinThread(Thread):
    def __init__(self, lock: Lock, event: Event, shared_queue: Queue, ip, port, user, passwd, name):
        Thread.__init__(self)
        self.name = name
        self.stopped = event
        self.queue = shared_queue
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.lock = lock
        logging.info("Connecting to %s on port %s" % (self.ip, self.port))
        self.client = GridcoinClient(ip=self.ip, port=self.port, user=self.user, passwd=self.passwd)

    def run(self):
        while not self.stopped.wait(10):
            self.lock.acquire(blocking=True)
            for point in self.client.getGRCPoints():
                self.queue.put(point.to_dict())
            self.lock.release()
            logging.debug('Added points host %s, queue size now %d' % (self.ip, self.queue.qsize()))