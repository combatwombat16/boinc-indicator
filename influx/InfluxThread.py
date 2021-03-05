from threading import Thread
import logging

from influx.Collector import Collector


class InfluxThread(Thread):
    def __init__(self, event, shared_queue, database, db_host, name, port=8086):
        Thread.__init__(self)
        self.queue = shared_queue
        self.database = database
        self.db_host = db_host
        self.name = name
        self.port = port
        self.stopped = event
        logging.info('Connecting to InfluxDB at host %s and database %s' % (self.db_host, self.database))
        self.collector = Collector(database=self.database, host=self.db_host, port=self.port).__enter__()

    def __exit__(self):
        logging.debug("Draining pool one last time then exiting")
        data = []
        while not self.queue.empty():
            data.append(self.queue.get())
        self.collector.write_data(data)
        logging.info("Disconnecting from Influx host")
        self.collector.__exit__()

    def run(self):
        data = []
        while not self.stopped.wait(10):
            logging.debug('Draining %d points from the queue' % (self.queue.qsize()))
            while not self.queue.empty():
                data.append(self.queue.get())
            self.collector.write_data(data)

        self.__exit__()
