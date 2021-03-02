from boinc.rpc.enums._Enum import _Enum


class CpuSched(_Enum):
    """ values of ACTIVE_TASK::scheduler_state and ACTIVE_TASK::next_scheduler_state
        "SCHEDULED" is synonymous with "executing" except when CPU throttling
        is in use.
    """
    UNINITIALIZED = 0
    PREEMPTED = 1
    SCHEDULED = 2
