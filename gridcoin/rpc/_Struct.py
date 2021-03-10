import jsons


class _Struct(object):
    """
    Helper class to deal with parsing and printing RPC responses from Gridcoin Wallet
    """
    def __str__(self, indent=0):
        return jsons.dumps(self, indent=0)
