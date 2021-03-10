import requests
import jsons

from gridcoin._Helpers import clean_dict


class Rpc(object):
    def __init__(self, ip, port, user, passwd):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd

    def call(self, method):
        payload = {'method': method}
        resp = requests.post('http://%s:%s' % (self.ip, self.port), json=payload, auth=(self.user, self.passwd))
        return resp.json()["result"]
