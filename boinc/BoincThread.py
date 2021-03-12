import logging
from threading import Thread, Event, Lock
from queue import Queue

from boinc.BoincClient import BoincClient


class BoincThread(Thread):
    def __init__(self, lock: Lock, event: Event, shared_queue: Queue, ip, name, passwd='boinc'):
        Thread.__init__(self)
        self.ip = ip
        self.name = name
        self.passwd = passwd
        self.queue = shared_queue
        self.stopped = event
        self.lock = lock
        logging.info('Creating BoincClient to host %s' % (self.ip))
        self.client = BoincClient(host=self.ip, passwd=self.passwd).__enter__()

    def __exit__(self, *args):
        logging.info('Disconnecting from Boinc host at %s' % (self.client))
        self.client.__exit__()

    def run(self):
        while not self.stopped.wait(5):
            self.lock.acquire(blocking=True)
            for point in self.client.getInfluxPoints():
                self.queue.put(point.to_dict())
            self.lock.release()
            logging.debug('Added points host %s, queue size now %d' % (self.ip, self.queue.qsize()))
        self.__exit__()
