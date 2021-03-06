from xml.etree import ElementTree

from boinc.rpc._Struct import _Struct
from boinc.rpc.CoProc import Coproc


class HostInfo(_Struct):
    def __init__(self):
        self.timezone = 0  # // local STANDARD time - UTC time (in seconds)
        self.domain_name = ""
        self.ip_addr = ""
        self.host_cpid = ""

        self.p_ncpus = 0  # // Number of CPUs on host
        self.p_vendor = ""  # // Vendor name of CPU
        self.p_model = ""  # // Model of CPU
        self.p_features = ""
        self.p_fpops = 0.0  # // measured floating point ops/sec of CPU
        self.p_iops = 0.0  # // measured integer ops/sec of CPU
        self.p_membw = 0.0  # // measured memory bandwidth (bytes/sec) of CPU
        # // The above are per CPU, not total
        self.p_calculated = 0.0  # // when benchmarks were last run, or zero
        self.p_vm_extensions_disabled = False

        self.m_nbytes = 0  # // Size of memory in bytes
        self.m_cache = 0  # // Size of CPU cache in bytes (L1 or L2?)
        self.m_swap = 0  # // Size of swap space in bytes

        self.d_total = 0  # // Total disk space on volume containing
        # // the BOINC client directory.
        self.d_free = 0  # // how much is free on that volume

        self.os_name = ""  # // Name of operating system
        self.os_version = ""  # // Version of operating system

        # // the following is non-empty if VBox is installed
        self.virtualbox_version = ""

        self.product_name = ""
        self.wsl_available = False

        self.coprocs = []  # COPROCS

        self.n_usable_coprocs = 0

        # The following are currently unused (not in RPC XML)
        self.serialnum = ""  # // textual description of coprocessors

    @classmethod
    def parse(cls, xml):
        if not isinstance(xml, ElementTree.Element):
            xml = ElementTree.fromstring(xml)

        # parse main XML
        hostinfo = super(HostInfo, cls).parse(xml)

        # parse each coproc in coprocs list
        aux = []
        for c in hostinfo.coprocs:
            aux.append(Coproc.parse(c))
        hostinfo.coprocs = aux

        return hostinfo
