from gridcoin.rpc._Struct import _Struct


class WalletInfo(_Struct):
    walletversion = 0
    balance = 0.0
    newmint = 0.0
    stake = 0.0
    keypoololdest = 0
    keypoolsize = 0
    staking = True
    mining_error = ''
