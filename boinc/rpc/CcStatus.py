from boinc.rpc._Struct import _Struct
from boinc.rpc.enums.NetworkStatus import NetworkStatus
from boinc.rpc.enums.SuspendReason import SuspendReason
from boinc.rpc.enums.RunMode import RunMode


class CcStatus(_Struct):
    def __init__(self):
        self.network_status = NetworkStatus.UNKNOWN
        self.ams_password_error = False
        self.manager_must_quit = False

        self.task_suspend_reason = SuspendReason.UNKNOWN  # // bitmap
        self.task_mode = RunMode.UNKNOWN
        self.task_mode_perm = RunMode.UNKNOWN  # // same, but permanent version
        self.task_mode_delay = 0.0  # // time until perm becomes actual

        self.network_suspend_reason = SuspendReason.UNKNOWN
        self.network_mode = RunMode.UNKNOWN
        self.network_mode_perm = RunMode.UNKNOWN
        self.network_mode_delay = 0.0

        self.gpu_suspend_reason = SuspendReason.UNKNOWN
        self.gpu_mode = RunMode.UNKNOWN
        self.gpu_mode_perm = RunMode.UNKNOWN
        self.gpu_mode_delay = 0.0

        self.disallow_attach = False
        self.simple_gui_only = False
        self.max_event_log_lines = 0
