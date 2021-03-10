import logging
from datetime import datetime
import jsons
import pytz

from gridcoin.rpc.Rpc import Rpc
from gridcoin.rpc.WalletInfo import WalletInfo
from gridcoin.rpc.Magnitudes import Magnitudes
from gridcoin.rpc.MiningInfo import MiningInfo
from gridcoin.rpc.BeaconStatus import BeaconStatus
from gridcoin.rpc.Info import Info
from gridcoin._Helpers import clean_dict
from influx.Point import Point


class GridcoinClient(object):
    def __init__(self, ip, port, user, passwd):
        self.rpc = Rpc(ip, port, user, passwd)

    def getWalletInfo(self):
        resp_json = self.rpc.call(method='getwalletinfo')
        return WalletInfo(**clean_dict(resp_json))

    def explainMagnitude(self):
        resp_json = self.rpc.call(method='explainmagnitude')
        return Magnitudes(resp_json)

    def getMiningInfo(self):
        resp_json = self.rpc.call(method='getmininginfo')
        return MiningInfo(**clean_dict(resp_json))

    def beaconStatus(self):
        resp_json = self.rpc.call(method='beaconstatus')
        return BeaconStatus(**clean_dict(resp_json))

    def getInfo(self):
        resp_json = self.rpc.call(method='getinfo')
        return Info(**clean_dict(resp_json))

    def getGRCPoints(self):
        points = []
        dt = datetime.now(tz=pytz.timezone('US/Pacific')).isoformat()
        mag = self.explainMagnitude()
        mining = self.getMiningInfo()
        for prj in mag.magnitude:
            point = Point(measurement='magnitude', time=dt)
            point.tags['project_name'] = prj.project
            point.fields['rac'] = prj.rac
            point.fields['magnitude'] = prj.magnitude
            points.append(point)

        mining_point = Point(measurement='mining', time=dt)
        mining_point.tags['CPID'] = mining.CPID
        mining_point.fields['blocks'] = mining.blocks
        mining_point.fields['magnitude'] = mining.current_magnitude
        mining_point.fields['current_difficulty'] = mining.difficulty.current
        mining_point.fields['pending_reward'] = mining.BoincRewardPending
        mining_point.fields['stake_weight'] = mining.stakeweight.valuesum
        mining_point.fields['time_to_stake'] = mining.time_to_stake_days
        mining_point.fields['staking_efficiency'] = mining.staking_efficiency
        points.append(mining_point)
        return points
