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
from time import sleep
from influx.Collector import Collector


hosts = [
    "192.168.1.220", "192.168.1.221", "192.168.1.222"
    , "192.168.1.223", "192.168.1.224", "192.168.1.225"
    , "192.168.1.230", "192.168.1.231"
    , "192.168.1.240", "192.168.1.241"
]
queueLock = Lock()
workQueue = queue.Queue(5000)


class HostThread(Thread):
    def __init__(self, event, shared_queue, ip, passwd='boinc'):
        Thread.__init__(self)
        self.ip = ip
        self.passwd = passwd
        self.queue = shared_queue
        self.stopped = event
        self.client = BoincClient(host=self.ip, passwd=self.passwd).__enter__()

    def __exit__(self, *args):
        self.client.__exit__()

    def run(self):
        while not self.stopped.wait(5):
            queueLock.acquire()
            for point in self.client.getInfluxPoints():
                self.queue.put(point.to_dict())
            queueLock.release()


def consumer(shared_queue):
    print('Queue size %d' % (shared_queue.qsize()))
    cnt = 0
    data = []
    while not shared_queue.empty():
        data.append(shared_queue.get())
        cnt += 1
    collector.write_data(data)
    print('Took %d out of queue.\nQueue now has %d items' % (cnt, shared_queue.qsize()))


if __name__ == '__main__':
    threads = []
    stopFlag = Event()

    with Collector(database="boinc_test", host="192.168.1.230", port=8086) as collector:
        for host in hosts:
            worker = HostThread(ip=host, shared_queue=workQueue, event=stopFlag)
            worker.start()
            threads.append(worker)

        for i in range(3):
            print('sleep %d' % (i))
            sleep(10)
            consumer(workQueue)

        stopFlag.set()
