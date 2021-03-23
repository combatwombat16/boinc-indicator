import logging
from threading import Thread, Event
from queue import Queue

from sense.SenseClient import SenseClient


class SenseThread(Thread):
    def __init__(self, event: Event, shared_queue: Queue, bucket, name, imperial_or_metric='metric', daemon=True):
        Thread.__init__(self, daemon=daemon)
        self.name = name
        self.queue = shared_queue
        self.stopped = event
        self.bucket = bucket
        self.imperial_or_metric = imperial_or_metric
        self.client = SenseClient()

    def run(self):
        while not self.stopped.wait(5):
            for point in self.client.getSensePoints(imperial_or_metric=self.imperial_or_metric, bucket=self.bucket):
                self.queue.put(point, block=True, timeout=.5)
            logging.debug('Added sense point to queue')
