from datetime import datetime
import pytz
from sense_hat import SenseHat
from influxdb_client import Point

from sense._Helpers import convertCToF, convertmbToPSI


class SenseClient(object):
    def __init__(self):
        self.sense = SenseHat()
        self.sense.clear()
        self.sense.set_imu_config(True, True, True)

    def getSensePoints(self, imperial_or_metric, bucket):
        dt = datetime.now(tz=pytz.timezone('US/Pacific')).isoformat()
        point = Point(measurement_name="sense")
        point.time(time=dt)
        # % relative
        point.field("humidity", self.sense.get_humidity())
        if imperial_or_metric == "imperial":
            point.field("temperature_from_humidity", convertCToF(self.sense.get_temperature_from_humidity()))
            point.field("temperature_from_pressure", convertCToF(self.sense.get_temperature_from_pressure()))
            point.field("pressure", convertmbToPSI(self.sense.get_pressure()))
        else:
            point.field("temperature_from_humidity", self.sense.get_temperature_from_humidity())
            point.field("temperature_from_pressure", self.sense.get_temperature_from_pressure())
            point.field("pressure", self.sense.get_pressure())
        point.field("orientation_radians", self.sense.get_orientation_radians())
        point.field("orientation_degress", self.sense.get_orientation_degrees())
        # magnetic intensity in microteslas
        point.field("compass_raw", self.sense.get_compass_raw())
        # rotational intensity in radians per second
        point.field("gyroscope_raw", self.sense.get_gyroscope_raw())
        # acceleration intensity in Gs
        point.field("accelerometer_raw", self.sense.get_accelerometer_raw())
        return [{"bucket": bucket, "point": point}]
