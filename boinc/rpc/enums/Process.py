from boinc.rpc.enums._Enum import _Enum


class Process(_Enum):
    """ values of ACTIVE_TASK::task_state """
    UNINITIALIZED = 0
    # // process doesn't exist yet
    EXECUTING = 1
    # // process is running, as far as we know
    SUSPENDED = 9
    # // we've sent it a "suspend" message
    ABORT_PENDING = 5
    # // process exceeded limits; send "abort" message, waiting to exit
    QUIT_PENDING = 8
    # // we've sent it a "quit" message, waiting to exit
    COPY_PENDING = 10
    # // waiting for async file copies to finish
