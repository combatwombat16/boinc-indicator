from gridcoin.rpc._Struct import _Struct


class SideStaking(_Struct):
    def __init__(self
                 , side_staking_enabled=False):
        self.side_staking_enabled = side_staking_enabled
