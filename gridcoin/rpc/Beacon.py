from gridcoin.rpc._Struct import _Struct


class Beacon(_Struct):
    def __init__(self
                 , cpid=''
                 , active=True
                 , pending=False
                 , expired=False
                 , renewable=False
                 , timestamp=""
                 , address=""
                 , public_key=""
                 , private_key_available=True
                 , magnitude=0
                 , verification_code=""
                 , is_mine=True):
        self.cpid = cpid
        self.active = active
        self.pending = pending
        self.expired = expired
        self.renewable = renewable
        self.timestamp = timestamp
        self.address = address
        self.public_key = public_key
        self.private_key_available = private_key_available
        self.magnitude = magnitude
        self.verification_code = verification_code
        self.is_mine = is_mine
