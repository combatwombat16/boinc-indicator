import logging
from datetime import datetime

from gridcoin.rpc.Rpc import Rpc
from gridcoin.rpc.WalletInfo import WalletInfo
from gridcoin.rpc.Magnitude import Magnitude
from gridcoin.rpc.MiningInfo import MiningInfo
from gridcoin.rpc.BeaconStatus import BeaconStatus
from influx.Point import Point


class GridcoinClient(object):
    def __init__(self, ip, port, user, passwd):
        self.rpc = Rpc(ip, port, user, passwd)

    def getWalletInfo(self):
        resp_json = self.rpc.call(method='getwalletinfo')
        return WalletInfo.parse(resp_json)

    def explainMagnitude(self):
        resp_json = self.rpc.call(method='explainmagnitude')
        return [Magnitude.parse(entry) for entry in resp_json]

    def getMiningInfo(self):
        resp_json = self.rpc.call(method='getmininginfo')
        return MiningInfo.parse(resp_json)

    def beaconStatus(self):
        resp_json = self.rpc.call(method='beaconstatus')
        return BeaconStatus.parse(resp_json)

    def getGRCPoints(self):
        points = []
        return points