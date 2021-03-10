from gridcoin.rpc._Struct import _Struct


class StakeSplitting(_Struct):
    def __init__(self
                 , stake_splitting_enabled=False):
        self.stake_splitting_enabled = stake_splitting_enabled
