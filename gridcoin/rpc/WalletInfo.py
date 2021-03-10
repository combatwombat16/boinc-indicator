from gridcoin.rpc._Struct import _Struct


class WalletInfo(_Struct):
    def __init__(self
                 , walletversion=0
                 , balance=0.0
                 , newmint=0.0
                 , stake=0.0
                 , keypoololdest=0
                 , keypoolsize=0
                 , staking=True
                 , mining_error=''):
        self.walletversion = walletversion
        self.balance = balance
        self.newmint = newmint
        self.stake = stake
        self.keypoololdest = keypoololdest
        self.keypoolsize = keypoolsize
        self.staking = staking
        self.mining_error = mining_error

