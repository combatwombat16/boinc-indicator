from threading import Thread
import logging

from boinc.BoincClient import BoincClient


class BoincThread(Thread):
    def __init__(self, event, shared_queue, ip, passwd='boinc'):
        Thread.__init__(self)
        self.ip = ip
        self.passwd = passwd
        self.queue = shared_queue
        self.stopped = event
        logging.info('Creating BoincClient to host %s' % (self.ip))
        self.client = BoincClient(host=self.ip, passwd=self.passwd).__enter__()

    def __exit__(self, *args):
        logging.info('Disconnecting from Boinc host at %s' % (self.client))
        self.client.__exit__()

    def run(self):
        while not self.stopped.wait(5):
            for point in self.client.getInfluxPoints():
                self.queue.put(point.to_dict())
            logging.debug('Added points host %s, queue size now %d' % (self.ip, self.queue.qsize()))
        self.__exit__()
