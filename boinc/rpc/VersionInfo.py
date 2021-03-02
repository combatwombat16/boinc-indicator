from functools import total_ordering
import json
from boinc.rpc._Struct import _Struct


@total_ordering
class VersionInfo(_Struct):
    def __init__(self, major=0, minor=0, release=0):
        self.major     = major
        self.minor     = minor
        self.release   = release

    @property
    def _tuple(self):
        return (self.major, self.minor, self.release)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._tuple == other._tuple

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._tuple > other._tuple

    #def __str__(self):
        #prep_dict = dict()
        #prep_dict['version'] = "%d.%d.%d" % (self.major, self.minor, self.release)

        #return jsons.dumps(prep_dict)

    #def __repr__(self):
    #    return "%s%r" % (self.__class__.__name__, self._tuple)

