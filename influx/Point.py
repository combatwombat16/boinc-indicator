from datetime import datetime
import jsons


class Point(object):
    measurement = ""
    tags = dict()
    time = ""
    fields = dict()

    def __init__(self, measurement="", tags=None, fields=None, time=datetime.now().isoformat()):
        if fields is None:
            fields = dict()
        if tags is None:
            tags = dict()
        self.measurement = measurement
        self.tags = tags
        self.fields = fields
        self.time = time

    def __str__(self):
        return jsons.dumps(self)

    def to_dict(self):
        return {"measurement": self.measurement, "tags": self.tags, "fields": self.fields, "time": self.time}