from gridcoin.rpc._Struct import _Struct


class Beacon(_Struct):
    cpid = ''
    active = True
    pending = False
    expired = False
    renewable = False
    timestamp = ""
    address = ""
    public_key = ""
    private_key_available = True
    magnitude = 0
    verification_code = ""
    is_mine = True
