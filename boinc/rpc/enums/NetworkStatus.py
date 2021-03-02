from boinc.rpc.enums._Enum import _Enum


class NetworkStatus(_Enum):
    """ Values of "network_status" """
    ONLINE = 0  # // have network connections open
    WANT_CONNECTION = 1  # // need a physical connection
    WANT_DISCONNECT = 2  # // don't have any connections, and don't need any
    LOOKUP_PENDING = 3  # // a website lookup is pending (try again later)

    @classmethod
    def name(cls, v):
        if v == cls.UNKNOWN:
            return "unknown"
        elif v == cls.ONLINE:
            return "online"  # misleading
        elif v == cls.WANT_CONNECTION:
            return "need connection"
        elif v == cls.WANT_DISCONNECT:
            return "don't need connection"
        elif v == cls.LOOKUP_PENDING:
            return "reference site lookup pending"
        else:
            return super(NetworkStatus, cls).name(v)
