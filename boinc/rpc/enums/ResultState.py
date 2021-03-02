from boinc.rpc.enums._Enum import _Enum


class ResultState(_Enum):
    """ Values of RESULT::state in client.
        THESE MUST BE IN NUMERICAL ORDER
        (because of the > comparison in RESULT::computing_done())
        see html/inc/common_defs.inc
    """
    NEW = 0
    # // New result
    FILES_DOWNLOADING = 1
    # // Input files for result (WU, app version) are being downloaded
    FILES_DOWNLOADED = 2
    # // Files are downloaded, result can be (or is being) computed
    COMPUTE_ERROR = 3
    # // computation failed; no file upload
    FILES_UPLOADING = 4
    # // Output files for result are being uploaded
    FILES_UPLOADED = 5
    # // Files are uploaded, notify scheduling server at some point
    ABORTED = 6
    # // result was aborted
    UPLOAD_FAILED = 7
    # // some output file permanent failure
