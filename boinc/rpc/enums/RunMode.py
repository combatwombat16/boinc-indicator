from boinc.rpc.enums._Enum import _Enum


class RunMode(_Enum):
    """ Run modes for CPU, GPU, network,
        controlled by Activity menu and snooze button
    """
    ALWAYS = 1
    AUTO = 2
    NEVER = 3
    RESTORE = 4

    # // restore permanent mode - used only in set_X_mode() GUI RPC

    @classmethod
    def name(cls, v):
        # all other modes use the fallback name
        if v == cls.AUTO:
            return "according to prefs"
        else:
            return super(RunMode, cls).name(v)
