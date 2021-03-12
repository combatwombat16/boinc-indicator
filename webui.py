import logging
from time import sleep
from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields

import api.constants as const
from boinc.BoincThread import BoincThread
from influx.InfluxThread import InfluxThread
from gridcoin.GridcoinThread import GridcoinThread

logging.basicConfig(filename='./webui.log', level=logging.DEBUG, filemode='w')

flask_app = Flask(__name__)
flask_app.config["DEBUG"] = True

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
            queue = const.gridcoin_work_queue
            event = const.gridcoin_consumer_stop_event
            user = const.gridcoin_user
            passwd = const.gridcoin_pass
            port = const.gridcoin_port
            thread_group = const.gridcoin_producer_threads
            lock = const.gridcoin_lock
        elif component.lower() == 'boinc':
            hosts = const.boinc_hosts
            queue = const.boinc_work_queue
            event = const.boinc_producer_stop_event
            thread_group = const.boinc_producer_threads
            lock = const.boinc_lock
        else:
            app.abort(400)
        if action.lower() == 'start':
            logging.debug("starting %s threads" % (component))
            for host in hosts:
                thread_name = '%s_%s_thread' % (component, host)
                event.clear()
                if component == 'boinc':
                    worker = BoincThread(ip=host
                                         , lock=lock
                                         , shared_queue=queue
                                         , event=event
                                         , name=thread_name)
                elif component == 'grc':
                    worker = GridcoinThread(ip=host
                                            , port=port
                                            , user=user
                                            , passwd=passwd
                                            , lock=lock
                                            , event=event
                                            , shared_queue=queue
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
            [{'name': thread.name, 'is_alive': thread.is_alive()} for thread in const.boinc_consumer_threads])

    @app.response(400, 'Invalid action specified')
    def put(self, action):
        if action.lower() == 'start':
            logging.debug("starting influxdb threads")
            for host in const.influxdb_hosts:
                const.boinc_consumer_stop_event.clear()
                influx_boinc_worker = InfluxThread(db_host=host
                                                   , lock=const.boinc_lock
                                                   , database=const.influxdb_boinc_database
                                                   , shared_queue=const.boinc_work_queue
                                                   , event=const.boinc_consumer_stop_event
                                                   , name="influx_" + host + "_" + const.influxdb_boinc_database)
                influx_boinc_worker.start()
                const.boinc_consumer_threads.append(influx_boinc_worker)
                influx_grc_worker = InfluxThread(db_host=host
                                                 , lock=const.gridcoin_lock
                                                 , database=const.influxdb_grc_database
                                                 , shared_queue=const.gridcoin_work_queue
                                                 , event=const.boinc_consumer_stop_event
                                                 , name="influx_" + host + "_" + const.influxdb_grc_database)
                influx_grc_worker.start()
                const.boinc_consumer_threads.append(influx_grc_worker)

            return self.get()
        elif action.lower() == 'stop':
            logging.debug("stopping influxdb threads")
            const.boinc_consumer_stop_event.set()
            const.boinc_consumer_threads.clear()
            return self.get()
        elif action.lower() == 'list':
            logging.debug("listing influxdb threads")
            return self.get()
        else:
            app.abort(400)


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=1672)
