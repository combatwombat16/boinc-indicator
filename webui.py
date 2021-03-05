from flask import Flask, jsonify
from flask_restplus import Api, Resource, fields
import api.constants as const
from boinc.BoincThread import BoincThread
from influx.InfluxThread import InfluxThread
import logging

logging.basicConfig(filename='./webui.log', level=logging.DEBUG, filemode='w')

flask_app = Flask(__name__)
flask_app.config["DEBUG"] = True

app = Api(app=flask_app
          , swagger="2.0"
          , version="0.1.0"
          , title="Boinc API"
          , description="API to interact with Boinc and InfluxDB"
          , license="MIT"
          , license_url="https://opensource.org/licenses/MIT"
          , contact_email="combatwombat16@gmail.com")

thread_info = app.model("threads", {
    'name': fields.String(description="Thread name", required=True)
    , 'is_alive': fields.Boolean(description='Thread status', required=True)
})


@app.route('/')
class Home(Resource):
    def get(self):
        return "<h1>Boinc API</h1><p>This API interacts with Boinc and InfluxDB to capture statistics for visualization.</p>"


@app.route('/boinc/hosts')
class GetBoincNodes(Resource):
    def get(self):
        return jsonify(const.boinc_hosts)


@app.route('/boinc/threads/<string:action>')
@app.doc(params={'action': '"list", "start" or "stop" threads'}, model=thread_info)
class ControlBoincThreads(Resource):
    @app.hide
    def get(self, action='list'):
        return jsonify([{"name": thread.name, "is_alive": thread.is_alive()} for thread in const.producer_threads])

    @app.response(400, 'Invalid action specified')
    def put(self, action):
        if action.lower() == 'start':
            logging.debug("starting boinc threads")
            for host in const.boinc_hosts:
                const.producerStopEvent.clear()
                boinc_worker = BoincThread(ip=host
                                           , shared_queue=const.workQueue
                                           , event=const.producerStopEvent
                                           , name="boinc_" + host + '_thread')
                boinc_worker.start()
                const.producer_threads.append(boinc_worker)
            return self.get()
        elif action.lower() == 'stop':
            logging.debug("stopping boinc threads")
            const.producerStopEvent.set()
            const.producer_threads.clear()
            return self.get()
        elif action.lower() == 'list':
            logging.debug(("listing boinc threads"))
            return self.get()
        else:
            app.abort(400)


@app.route('/influxdb/hosts')
class GetInfluxdbHosts(Resource):
    def get(self):
        return jsonify(const.influxdb_hosts)


@app.route('/influxdb/threads/<string:action>')
@app.doc(params={'action': '"list", "start" or "stop" threads'}, model=thread_info)
class ControlInfluxThreads(Resource):
    @app.hide
    def get(self, action='list'):
        return jsonify([{'name': thread.name, 'is_alive': thread.is_alive()} for thread in const.consumer_threads])

    @app.response(400, 'Invalid action specified')
    def put(self, action):
        if action.lower() == 'start':
            logging.debug("starting influxdb threads")
            for host in const.influxdb_hosts:
                const.consumerStopEvent.clear()
                influx_worker = InfluxThread(db_host=host
                                             , database=const.influxdb_database
                                             , shared_queue=const.workQueue
                                             , event=const.consumerStopEvent
                                             , name="influx_" + host + "_name")
                influx_worker.start()
                const.consumer_threads.append(influx_worker)
            return self.get()
        elif action.lower() == 'stop':
            logging.debug("stopping influxdb threads")
            const.consumerStopEvent.set()
            const.consumer_threads.clear()
            return self.get()
        elif action.lower() == 'list':
            logging.debug("listing influxdb threads")
            return self.get()
        else:
            app.abort(400)


if __name__ == '__main__':
    flask_app.run()
