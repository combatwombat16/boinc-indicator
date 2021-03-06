from xml.etree import ElementTree
import time
import jsons

from boinc._Helpers import setattrs_from_xml
from boinc.rpc._Struct import _Struct
from boinc.rpc.enums.ResultState import ResultState
from boinc.rpc.enums.Process import Process
from boinc.rpc.enums.CpuSched import CpuSched


class Result(_Struct):
    """ Also called "task" in some contexts """

    def __init__(self):
        # Names and values follow lib/gui_rpc_client.h @ RESULT
        # Order too, except when grouping contradicts client/result.cpp
        # RESULT::write_gui(), then XML order is used.

        self.name = ""
        self.wu_name = ""
        self.version_num = 0
        # // identifies the app used
        self.plan_class = ""
        self.project_url = ""  # from PROJECT.master_url
        self.report_deadline = 0.0  # seconds since epoch
        self.received_time = 0.0  # seconds since epoch
        # // when we got this from server
        self.ready_to_report = False
        # // we're ready to report this result to the server;
        # // either computation is done and all the files have been uploaded
        # // or there was an error
        self.got_server_ack = False
        # // we've received the ack for this result from the server
        self.final_cpu_time = 0.0
        self.final_elapsed_time = 0.0
        self.state = ResultState.NEW
        self.estimated_cpu_time_remaining = 0.0
        # // actually, estimated elapsed time remaining
        self.exit_status = 0
        # // return value from the application
        self.suspended_via_gui = False
        self.project_suspended_via_gui = False
        self.edf_scheduled = False
        # // temporary used to tell GUI that this result is deadline-scheduled
        self.coproc_missing = False
        # // a coproc needed by this job is missing
        # // (e.g. because user removed their GPU board).
        self.scheduler_wait = False
        self.scheduler_wait_reason = ""
        self.network_wait = False
        self.resources = ""
        # // textual description of resources used

        # // the following defined if active
        # XML is generated in client/app.cpp ACTIVE_TASK::write_gui()
        self.active_task = False
        self.active_task_state = Process.UNINITIALIZED
        self.app_version_num = 0
        self.slot = -1
        self.pid = 0
        self.scheduler_state = CpuSched.UNINITIALIZED
        self.checkpoint_cpu_time = 0.0
        self.current_cpu_time = 0.0
        self.fraction_done = 0.0
        self.elapsed_time = 0.0
        self.swap_size = 0
        self.working_set_size_smoothed = 0.0
        self.too_large = False
        self.needs_shmem = False
        self.graphics_exec_path = ""
        self.web_graphics_url = ""
        self.remote_desktop_addr = ""
        self.slot_path = ""
        # // only present if graphics_exec_path is

        # The following are not in original API, but are present in RPC XML reply
        self.completed_time = 0.0
        # // time when ready_to_report was set
        self.report_immediately = False
        self.working_set_size = 0
        self.page_fault_rate = 0.0
        # // derived by higher-level code

        self.progress_rate = 0.0
        self.platform = ""
        self.bytes_sent = 0.0
        self.bytes_received = 0.0

        # The following are in API, but are NEVER in RPC XML reply. Go figure
        self.signal = 0

        self.app = None  # APP*
        self.wup = None  # WORKUNIT*
        self.project = None  # PROJECT*
        self.avp = None  # APP_VERSION*

    @classmethod
    def parse(cls, xml):
        if not isinstance(xml, ElementTree.Element):
            xml = ElementTree.fromstring(xml)

        # parse main XML
        result = super(Result, cls).parse(xml)

        # parse '<active_task>' children
        active_task = xml.find('active_task')
        if active_task is None:
            result.active_task = False  # already the default after __init__()
        else:
            result.active_task = True  # already the default after main parse
            result = setattrs_from_xml(result, active_task)

        # // if CPU time is nonzero but elapsed time is zero,
        # // we must be talking to an old client.
        # // Set elapsed = CPU
        # // (easier to deal with this here than in the manager)
        if result.current_cpu_time != 0 and result.elapsed_time == 0:
            result.elapsed_time = result.current_cpu_time

        if result.final_cpu_time != 0 and result.final_elapsed_time == 0:
            result.final_elapsed_time = result.final_cpu_time

        return result

    def __str__(self):
        prep = self
        prep.received_time = time.ctime(prep.received_time)
        prep.report_deadline = time.ctime(prep.report_deadline)

        return jsons.dumps(prep)
