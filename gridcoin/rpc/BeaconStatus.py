import jsons

from gridcoin.rpc._Struct import _Struct
from gridcoin.rpc.Beacon import Beacon


class BeaconStatus(_Struct):
    def __init__(self
                 , active: [Beacon]
                 , pending: [Beacon]):
        self.active = [Beacon(**bc) for bc in active]
        self.pending = [Beacon(**bc) for bc in pending]
