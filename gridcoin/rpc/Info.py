from gridcoin.rpc._Struct import _Struct
from gridcoin.rpc.Difficulty import Difficulty
from gridcoin._Helpers import clean_dict


class Info(_Struct):
    def __init__(self
                 , version=""
                 , minor_version=0
                 , protocolversion=0
                 , walletversion=0
                 , balance=0.0
                 , newmint=0.0
                 , stake=0.0
                 , blocks=0
                 , in_sync=True
                 , timeoffset=0
                 , uptime=0
                 , moneysupply=0.0
                 , connections=0
                 , proxy=""
                 , ip=""
                 , difficulty=None
                 , testnet=False
                 , keypoololdest=0
                 , keypoolsize=0
                 , paytxfee=0.0
                 , mininput=0.0
                 , errors=""):
        self.version = version
        self.minor_version = minor_version
        self.protocolversion = protocolversion
        self.walletversion = walletversion
        self.balance = balance
        self.newmint = newmint
        self.stake = stake
        self.blocks = blocks
        self.in_sync = in_sync
        self.timeoffset = timeoffset
        self.uptime = uptime
        self.moneysupply = moneysupply
        self.connections = connections
        self.proxy = proxy
        self.ip = ip
        if difficulty is None:
            difficulty = dict()
        self.difficulty = Difficulty(**clean_dict(difficulty))
        self.testnet = testnet
        self.keypoololdest = keypoololdest
        self.keypoolsize = keypoolsize
        self.paytxfee = paytxfee
        self.mininput = mininput
        self.errors = errors
