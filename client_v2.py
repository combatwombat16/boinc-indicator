#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# client.py - Somewhat higher-level GUI_RPC API for BOINC core client
#
#    Copyright (C) 2013 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. See <http://www.gnu.org/licenses/gpl.html>

# Based on client/boinc_cmd.cpp

from boinc.BoincClient import BoincClient
import queue
from threading import Thread, Event, Lock
from influx.Collector import Collector
import logging


hosts = [
    "192.168.1.220", "192.168.1.221", "192.168.1.222"
    , "192.168.1.223", "192.168.1.224", "192.168.1.225"
    , "192.168.1.230", "192.168.1.231"
    , "192.168.1.240", "192.168.1.241"
]
queueLock = Lock()
workQueue = queue.Queue(5000)
logging.basicConfig(filename='./client_v2.log', level=logging.DEBUG)


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
            queueLock.acquire()
            for point in self.client.getInfluxPoints():
                self.queue.put(point.to_dict())
            logging.debug('Added points host %s, queue size now %d' % (self.ip, self.queue.qsize()))
            queueLock.release()


class InfluxThread(Thread):
    def __init__(self, event, shared_queue, database, db_host, port=8086):
        Thread.__init__(self)
        self.queue = shared_queue
        self.database = database
        self.db_host = db_host
        self.port = port
        self.stopped = event
        logging.info('Connecting to InfluxDB at host %s and database %s' % (self.db_host, self.database))
        self.collector = Collector(database=self.database, host=self.db_host, port=self.port).__enter__()

    def __exit__(self):
        logging.info("Disconnecting from Influx host")
        self.collector.__exit__()

    def run(self):
        data = []
        while not self.stopped.wait(10):
            queueLock.acquire()
            logging.debug('Draining %d points from the queue' % (self.queue.qsize()))
            while not self.queue.empty():
                data.append(self.queue.get())
            queueLock.release()
            self.collector.write_data(data)


if __name__ == '__main__':
    threads = []
    stopFlag = Event()

    #with Collector(database="boinc_test", host="192.168.1.230", port=8086) as collector:
    for host in hosts:
        boinc_worker = BoincThread(ip=host
                                   , shared_queue=workQueue
                                   , event=stopFlag)
        boinc_worker.start()
        threads.append(boinc_worker)

    influx_worker = InfluxThread(event=stopFlag
                                 , shared_queue=workQueue
                                 , database='boinc_test'
                                 , db_host='192.168.1.230'
                                 , port=8086)

    influx_worker.start()

    threads.append(influx_worker)
    #stopFlag.set()
