from gridcoin.rpc._Struct import _Struct
from gridcoin.rpc.Beacon import Beacon


class BeaconStatus(_Struct):
    active = [Beacon()]
    pending = [Beacon()]