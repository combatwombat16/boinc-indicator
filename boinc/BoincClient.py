import socket
import hashlib
import pytz
from datetime import datetime

from boinc._Helpers import read_gui_rpc_password
from boinc.rpc.Rpc import Rpc
from boinc.rpc.CcStatus import CcStatus
from boinc.rpc.VersionInfo import VersionInfo
from boinc.rpc.Result import Result
from boinc.rpc.HostInfo import HostInfo
from boinc.rpc.Project import Project
from boinc.rpc.enums.RunMode import RunMode
from boinc.rpc.enums.ResultState import ResultState
from boinc.rpc.enums.Process import Process
from boinc.rpc.enums.CpuSched import CpuSched

from influx.Point import Point


class BoincClient(object):

    def __init__(self, host="", passwd=None):
        host = host.split(':', 1)

        self.hostname = host[0]
        self.port = int(host[1]) if len(host) == 2 else 0
        self.passwd = passwd
        self.rpc = Rpc(text_output=False)
        self.version = None
        self.authorized = False

        # Informative, not authoritative. Records status of *last* RPC call,
        # but does not infer success about the *next* one.
        # Thus, it should be read *after* an RPC call, not prior to one
        self.connected = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    def connect(self):
        try:
            self.rpc.connect(self.hostname, self.port)
            self.connected = True
        except socket.error:
            self.connected = False
            return
        self.authorized = self.authorize(self.passwd)
        self.version = self.exchange_versions()

    def disconnect(self):
        self.rpc.disconnect()

    def authorize(self, password):
        """ Request authorization. If password is None and we are connecting
            to localhost, try to read password from the local config file
            GUI_RPC_PASSWD_FILE. If file can't be read (not found or no
            permission to read), try to authorize with a blank password.
            If authorization is requested and fails, all subsequent calls
            will be refused with socket.error 'Connection reset by peer' (104).
            Since most local calls do no require authorization, do not attempt
            it if you're not sure about the password.
        """
        if password is None and not self.hostname:
            password = read_gui_rpc_password() or ""
        nonce = self.rpc.call('<auth1/>').text
        inputStr = '%s%s' % (nonce, password)
        hash = hashlib.md5(inputStr.encode('utf-8')).hexdigest().lower()
        reply = self.rpc.call('<auth2><nonce_hash>%s</nonce_hash></auth2>' % hash)

        if reply.tag == 'authorized':
            return True
        else:
            return False

    def exchange_versions(self):
        """ Return VersionInfo instance with core client version info """
        return VersionInfo.parse(self.rpc.call('<exchange_versions/>'))

    def get_cc_status(self):
        """ Return CcStatus instance containing basic status, such as
            CPU / GPU / Network active/suspended, etc
        """
        if not self.connected:
            self.connect()
        try:
            return CcStatus.parse(self.rpc.call('<get_cc_status/>'))
        except socket.error:
            self.connected = False

    def get_host_info(self):
        """ Get information about host hardware and usage. """
        return HostInfo.parse(self.rpc.call('<get_host_info/>'))

    def get_tasks(self):
        """ Same as get_results(active_only=False) """
        return self.get_results(False)

    def get_results(self, active_only=False):
        """ Get a list of results.
            Those that are in progress will have information such as CPU time
            and fraction done. Each result includes a name;
            Use CC_STATE::lookup_result() to find this result in the current static state;
            if it's not there, call get_state() again.
        """
        reply = self.rpc.call("<get_results><active_only>%d</active_only></get_results>"
                              % (1 if active_only else 0))
        if not reply.tag == 'results':
            return []

        results = []
        for item in list(reply):
            results.append(Result.parse(item))

        return results

    def get_projects(self):
        reply = self.rpc.call("<get_project_status/>")

        if not reply or not reply.tag == 'projects':
            return []

        projects = []
        for item in list(reply):
            projects.append(Project.parse(item))

        return projects

    def set_mode(self, component, mode, duration=0):
        """ Do the real work of set_{run,gpu,network}_mode()
            This method is not part of the original API.
            Valid components are 'run' (or 'cpu'), 'gpu', 'network' (or 'net')
        """
        component = component.replace('cpu', 'run')
        component = component.replace('net', 'network')
        try:
            reply = self.rpc.call("<set_%s_mode>"
                                  "<%s/><duration>%f</duration>"
                                  "</set_%s_mode>"
                                  % (component,
                                     RunMode.name(mode).lower(), duration,
                                     component))
            return (reply.tag == 'success')
        except socket.error:
            return False

    def set_run_mode(self, mode, duration=0):
        """ Set the run mode (RunMode.NEVER/AUTO/ALWAYS/RESTORE)
            NEVER will suspend all activity, including CPU, GPU and Network
            AUTO will run according to preferences.
            If duration is zero, mode is permanent. Otherwise revert to last
            permanent mode after duration seconds elapse.
        """
        return self.set_mode('cpu', mode, duration)

    def set_gpu_mode(self, mode, duration=0):
        """ Set the GPU run mode, similar to set_run_mode() but for GPU only
        """
        return self.set_mode('gpu', mode, duration)

    def set_network_mode(self, mode, duration=0):
        """ Set the Network run mode, similar to set_run_mode()
            but for network activity only
        """
        return self.set_mode('net', mode, duration)

    def run_benchmarks(self):
        """ Run benchmarks. Computing will suspend during benchmarks """
        return self.rpc.call('<run_benchmarks/>').tag == "success"

    def quit(self):
        """ Tell the core client to exit """
        if self.rpc.call('<quit/>').tag == "success":
            self.connected = False
            return True
        return False

    def getInfluxPoints(self):
        """ Build data points for transmission to InfluxDB for project and task monitoring. """
        points = []
        # Get info from boinc client
        hostInfo = self.get_host_info()
        dt = datetime.now(tz=pytz.timezone('US/Pacific')).isoformat()
        rs = ResultState()
        ps = Process()
        cs = CpuSched()
        results = self.get_results(True)
        projects = self.get_projects()
        for result in results:
            # Create new point
            point = Point(measurement='task', time=dt)
            # Set tags
            point.tags['host'] = hostInfo.domain_name
            point.tags['ip_address'] = hostInfo.ip_addr
            point.tags['project_name'] = [project.project_name for project in projects
                                          if project.master_url == result.project_url][0]
            point.tags['state'] = rs.name(result.state)
            point.tags['active_task_state'] = ps.name(result.active_task_state)
            point.tags['scheduler_state'] = cs.name(result.scheduler_state)
            point.tags['task_name'] = result.name
            # Set fields
            point.fields['elapsed_time'] = result.elapsed_time
            point.fields['fraction_done'] = result.fraction_done
            point.fields['swap_size'] = result.swap_size
            tmp_res = result.resources.split("+")
            cpu = tmp_res[0].strip().split(" ")[0]
            point.fields['cpu'] = float(cpu) if cpu != '' else 0.0
            point.fields['gpu'] = 1 if len(tmp_res) > 1 else 0
            points.append(point)

        for project in projects:
            # Create new point
            point = Point(measurement='project', time=dt)
            # Set tags
            point.tags['host'] = hostInfo.domain_name
            point.tags['ip_address'] = hostInfo.ip_addr
            point.tags['project_name'] = project.project_name
            # Set fields
            point.fields['host_total_credit'] = project.host_total_credit
            point.fields['host_average_credit'] = project.host_expavg_credit
            point.fields['user_total_credit'] = project.user_total_credit
            point.fields['user_average_credit'] = project.user_expavg_credit
            point.fields['completed_jobs'] = project.njobs_success
            point.fields['failed_jobs'] = project.njobs_error
            points.append(point)

        return points
