from gridcoin.rpc._Struct import _Struct
from gridcoin.rpc.Magnitude import Magnitude


class Magnitudes(_Struct):
    def __init__(self
                 , magnitude: [Magnitude]):
        self.magnitude = [Magnitude(**mag) for mag in magnitude]