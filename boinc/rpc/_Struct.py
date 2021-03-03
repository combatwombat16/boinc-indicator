import jsons

from boinc._Helpers import setattrs_from_xml


class _Struct(object):
    """ base helper class with common methods for all classes derived from
        BOINC's C++ structs
    """
    @classmethod
    def parse(cls, xml):
        return setattrs_from_xml(cls(), xml)

    def __str__(self, indent=0):
        return jsons.dumps(self)
