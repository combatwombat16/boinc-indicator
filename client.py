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

import gui_rpc_client

class BoincClient(object):

    def __init__(self, **kwargs):
        self.rpc = gui_rpc_client.RpcClient()

        host = kwargs.setdefault('host', "").split(':', 1)

        self.hostname = host[0]
        self.port     = int(host[1]) if len(host)==2 else 0

        self.passwd   = kwargs.setdefault('passwd',
                                          gui_rpc_client.read_gui_rpc_password())

        self.rpc.init(self.hostname, self.port)

        if self.passwd:
            self.rpc.authorize(self.passwd)

        self.version = self.rpc.exchange_versions()
