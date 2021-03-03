import time
import jsons
from xml.etree import ElementTree

from boinc.rpc._Struct import _Struct


class Project(_Struct):
    def __init__(self):
        self.master_url = ""
        self.project_name = ""
        self.symstore = None
        self.user_name = ""
        self.team_name = ""
        self.host_venue = None
        self.email_hash = ""
        self.cross_project_id = ""
        self.external_cpid = ""
        self.cpid_time = 0.0

        self.user_total_credit = 0.0
        self.user_expavg_credit = 0.0
        self.user_create_time = 0.0

        self.rpc_seqno = 0

        self.userid = 0
        self.teamid = 0
        self.hostid = 0

        self.host_total_credit = 0.0
        self.host_expavg_credit = 0.0
        self.host_create_time = 0.0

        self.min_rpc_time = 0.0
        self.next_rpc_time = 0.0

        self.nrpc_failures = None
        self.master_fetch_failures = None

        self.rec = 0.0

        self.rec_time = 0.0
        self.resource_share = 0.0
        self.desired_disk_usage = 0.0
        self.disk_usage = 0.0

        self.duration_correction_factor = 0.0

        self.sched_rpc_pending = 0
        self.send_time_stats_log = 0
        self.send_job_log = 0

        self.njobs_success = 0
        self.njobs_error = 0

        self.elapsed_time = 0.0
        self.last_rpc_time = 0.0
        self.dont_use_dcf = None

        self.rsc_backoff_time = None
        self.rsc_backoff_interval = None

        self.dont_request_more_work = None

        self.verify_files_on_app_start = None

        self.gui_urls = []

        self.sched_priority = 0.0
        self.project_files_downloaded_time = 0.0
        self.project_dir = ""

        self.attached_via_acct_mgr = True
        self.no_rsc_ams = ""
        self.no_rsc_pref = ""
        self.ams_resource_share_new = ""
        self.disk_share = ""
        self.send_full_workload = False
        self.no_rsc_apps = ""
        self.scheduler_rpc_in_progress = True

        self.venue = None

    @classmethod
    def parse(cls, xml):
        if not isinstance(xml, ElementTree.Element):
            xml = ElementTree.fromstring(xml)

        # parse main XML
        result = super(Project, cls).parse(xml)

        return result

    def __str__(self):
        prep = self
        prep.rec_time = time.ctime(prep.rec_time)
        prep.user_create_time = time.ctime(prep.user_create_time)
        prep.host_create_time = time.ctime(prep.host_create_time)

        return jsons.dumps(prep)
