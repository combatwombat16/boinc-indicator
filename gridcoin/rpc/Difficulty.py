from gridcoin.rpc._Struct import _Struct


class Difficulty(_Struct):
    def __init__(self
                 , current=0.0
                 , target=0.0
                 , last_search_interval=0):
        self.current = current
        self.target = target
        self.last_search_interval = last_search_interval
