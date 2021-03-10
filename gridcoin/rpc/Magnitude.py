from gridcoin.rpc._Struct import _Struct


class Magnitude(_Struct):
    def __init__(self
                 , project=''
                 , rac=0.0
                 , magnitude=0.0):
        self.project = project
        self.rac = rac
        self.magnitude = magnitude
