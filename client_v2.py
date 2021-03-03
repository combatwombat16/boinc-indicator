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

import logging
from time import sleep
import queue
from threading import Event

from boinc.BoincThread import BoincThread
from influx.InfluxThread import InfluxThread


hosts = [
    "192.168.1.220", "192.168.1.221", "192.168.1.222"
    , "192.168.1.223", "192.168.1.224", "192.168.1.225"
    , "192.168.1.230", "192.168.1.231"
    , "192.168.1.240", "192.168.1.241"
]
workQueue = queue.Queue(5000)
logging.basicConfig(filename='./client_v2.log', level=logging.DEBUG, filemode='w')


if __name__ == '__main__':
    threads = []
    stopBoincFlag = Event()
    stopInfluxFlag = Event()

    for host in hosts:
        boinc_worker = BoincThread(ip=host
                                   , shared_queue=workQueue
                                   , event=stopBoincFlag)
        boinc_worker.start()
        threads.append(boinc_worker)

    influx_worker = InfluxThread(event=stopInfluxFlag
                                 , shared_queue=workQueue
                                 , database='boinc_test'
                                 , db_host='192.168.1.230'
                                 , port=8086)

    influx_worker.start()

    threads.append(influx_worker)

    sleep(30)
    stopBoincFlag.set()
    sleep(3)
    stopInfluxFlag.set()
