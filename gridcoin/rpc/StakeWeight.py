from gridcoin.rpc._Struct import _Struct


class StakeWeight(_Struct):
    def __init__(self
                 , minimum=0
                 , maximum=0
                 , combined=0
                 , valuesum=0.0
                 , legacy=0.0):
        self.minimum = minimum
        self.maximum = maximum
        self.combined = combined
        self.valuesum = valuesum
        self.legacy = legacy
