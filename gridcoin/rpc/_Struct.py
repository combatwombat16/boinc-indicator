import jsons


class _Struct(object):
    """
    Helper class to deal with parsing and printing RPC responses from Gridcoin Wallet
    """
    @classmethod
    def parse(cls, json_in):
        tmp_cls = cls()
        for key in list(json_in.keys()):
            if not isinstance(key, str):
                continue
            value = json_in[key]
            del json_in[key]
            json_in[key.replace("-", "_").replace(" ", "_")] = value
        for key in list(json_in.keys()):
            setattr(tmp_cls, key, json_in[key])
        return tmp_cls

    def __str__(self, indent=0):
        return jsons.dumps(self, indent=0)
