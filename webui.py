import logging
from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields

from api.Constants import Constants
from boinc.BoincThread import BoincThread
from influx.InfluxThread import InfluxThread
from gridcoin.GridcoinThread import GridcoinThread
from sense.SenseThread import SenseThread

logging.basicConfig(filename='./webui.log', level=logging.DEBUG, filemode='w')

flask_app = Flask(__name__)
flask_app.config["DEBUG"] = True

const = Constants()

app = Api(app=flask_app
          , swagger="2.0"
          , version="0.1.0"
          , title="Boinc API"
          , description="API to interact with Boinc and InfluxDB"
          , license="GPLv3+"
          , license_url="http://www.gnu.org/licenses/gpl-3.0.html"
          , contact_email="combatwombat16@gmail.com")

thread_info = app.model("threads", {
    'name': fields.String(description="Thread name", required=True)
    , 'is_alive': fields.Boolean(description='Thread status', required=True)
})


@app.route('/hosts/<string:component>')
@app.doc(params={'component': '"influxdb", "grc" or "boinc"'})
class GetHostInfo(Resource):
    @app.response(400, 'Invalid component specified')
    def get(self, component):
        if component.lower() == 'grc':
            return jsonify(const.gridcoin_hosts)
        elif component.lower() == 'boinc':
            return jsonify(const.boinc_hosts)
        elif component.lower() == 'influxdb':
            return jsonify(const.influxdb_hosts)
        else:
            app.abort(400)


@app.route('/producer/threads/<string:component>/<string:action>')
@app.doc(params={'component': '"grc" or "boinc"', 'action': '"list", "start" or "stop" threads'}, model=thread_info)
class ControlProducerThreads(Resource):
    @app.hide
    @app.response(400, 'Invalid parameter specified')
    def get(self, component, action='list'):
        if component.lower() == 'grc':
            return jsonify(
                [{"name": thread.name, "is_alive": thread.is_alive()} for thread in const.gridcoin_producer_threads])
        elif component.lower() == 'boinc':
            return jsonify(
                [{"name": thread.name, "is_alive": thread.is_alive()} for thread in const.boinc_producer_threads])
        else:
            app.abort(400)

    @app.response(400, 'Invalid parameter specified')
    def put(self, component, action):
        if component.lower() == 'grc':
            hosts = const.gridcoin_hosts
            queue = const.work_queue
            event = const.gridcoin_producer_stop_event
            user = const.gridcoin_user
            passwd = const.gridcoin_pass
            port = const.gridcoin_port
            thread_group = const.gridcoin_producer_threads
            bucket = const.influxdb_grc_bucket
        elif component.lower() == 'boinc':
            hosts = const.boinc_hosts
            queue = const.work_queue
            event = const.boinc_producer_stop_event
            thread_group = const.boinc_producer_threads
            bucket = const.influxdb_boinc_bucket
        elif component.lower() == 'sense':
            hosts = const.sense_hosts
            event = const.sense_producer_stop_event
            thread_group = const.sense_producer_threads
            bucket = const.influxdb_sense_bucket
            queue = const.work_queue
        else:
            app.abort(400)
        if action.lower() == 'start':
            logging.debug("starting %s threads" % (component))
            for host in hosts:
                thread_name = '%s_%s_thread' % (component, host)
                event.clear()
                if component == 'boinc':
                    worker = BoincThread(ip=host
                                         , shared_queue=queue
                                         , event=event
                                         , name=thread_name
                                         , bucket=bucket)
                elif component == 'grc':
                    worker = GridcoinThread(ip=host
                                            , port=port
                                            , user=user
                                            , passwd=passwd
                                            , event=event
                                            , shared_queue=queue
                                            , name=thread_name
                                            , bucket=bucket)
                elif component == "sense":
                    worker = SenseThread(event=event
                                         , shared_queue=queue
                                         , bucket=bucket
                                         , name=thread_name)
                worker.start()
                thread_group.append(worker)
            return self.get(component)
        elif action.lower() == 'stop':
            logging.debug("stopping %s threads" % (component))
            event.set()
            thread_group.clear()
            return self.get(component)
        elif action.lower() == 'list':
            logging.debug(("listing %s threads" % (component)))
            return self.get(component)
        else:
            app.abort(400)


@app.route('/influxdb/threads/<string:action>')
@app.doc(params={'action': '"list", "start" or "stop" threads'}, model=thread_info)
class ControlInfluxThreads(Resource):
    @app.hide
    def get(self, action='list'):
        return jsonify(
            [{'name': thread.name, 'is_alive': thread.is_alive()} for thread in const.influxdb_consumer_threads])

    @app.response(400, 'Invalid action specified')
    def put(self, action):
        if action.lower() == 'start':
            logging.debug("starting influxdb threads")
            for host in const.influxdb_hosts:
                const.influxdb_consumer_stop_event.clear()
                influx_worker = InfluxThread(db_host=host
                                             , org=const.influxdb_org
                                             , token=const.influxdb_token
                                             , shared_queue=const.work_queue
                                             , event=const.influxdb_consumer_stop_event
                                             , name="influx_" + host + "_" + const.influxdb_org)
                influx_worker.start()
                const.influxdb_consumer_threads.append(influx_worker)

            return self.get()
        elif action.lower() == 'stop':
            logging.debug("stopping influxdb threads")
            const.influxdb_consumer_stop_event.set()
            const.influxdb_consumer_threads.clear()
            return self.get()
        elif action.lower() == 'list':
            logging.debug("listing influxdb threads")
            return self.get()
        else:
            app.abort(400)


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=1672)
