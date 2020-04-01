from flask import Flask, jsonify, request
from argparse import ArgumentParser
import json
import threading

app = Flask(__name__)
RECORDS = []
RECORD_LOCK = threading.Lock()


@app.route('/simpleservice/api/v1.0/status', methods=['GET'])
def get_status():
    """clients can use this method to see if service alive and kicking"""
    return "OK"     # defaults to a 200 HTML status return code


# standard URL for a REST API
@app.route('/simpleservice/api/v1.0/shutdown', methods=['POST'])
def shutdown():
    """clean method to shutdown down flask/web server"""
    shutdown_func = request.environ.get(
        'werkzeug.server.shutdown')     # default web server with flask
    if shutdown_func is None:
        return 'unable to shutdown server!', 501
    shutdown_func()
    return "server shutting down..."


# can also handle all methods in a single
@app.route('/simpleservice/api/v1.0/record', methods=['GET'])
# handler ['GET', 'POST, 'PUT', DELETE' ]
def get_records():
    """get a list of all dictionary records and return as a JSON file"""
    with RECORD_LOCK:               # since flask 1.0 multi-threaded is enabled by default
        return jsonify(RECORDS)


@app.route('/simpleservice/api/v1.0/record/<name>', methods=['GET'])
def get_record_by_name(name):
    """uses <name> construct in route to pass a record parameter to route handler"""
    with RECORD_LOCK:
        # return list of matches or []
        return jsonify([r for r in RECORDS if r.get('name') == name])


@app.route('/simpleservice/api/v1.0/record', methods=['POST'])
def add_record():
    """add a record to the global structure"""
    if 'json' not in request.files:
        # use an HTML record that seems appropriate
        return "no json file in the request!", 400
    try:
        # can't assume that JSON file is valid
        _record = json.loads(request.files['json'].read())
    except ValueError:
        return "failed to parse JSON file correctly!", 400
    if type(_record) is not dict or 'name' not in _record:
        return "expecting a dictionary with identifier, post failed!", 400
    with RECORD_LOCK:
        # just check if the name already exists in the global RECORD list
        if len([r for r in RECORDS if r.get('name') == _record['name']]):
            return "already in the records!", 409
        RECORDS.append(_record)
    return "OK"


@app.route('/simpleservice/api/v1.0/record', methods=['PUT'])
def update_record():
    """route that updates an existing record - expects a JSON file as input"""
    if 'json' not in request.files:
        return "no json file in the request!", 400
    try:
        _record = json.loads(request.files['json'].read())
    except ValueError:
        return "failed to parse JSON file correctly!", 400
    if type(_record) is not dict or 'name' not in _record:
        return "expecting a dictionary with a name, post failed!", 400
    with RECORD_LOCK:
        for _index, _rec in enumerate(RECORDS):
            if _rec['name'] == _record['name']:
                RECORDS[_index] = _record
                return "OK"
    return "Failed to update record!", 500


@app.route('/simpleservice/api/v1.0/record', methods=['DELETE'])
def remove_record():
    """route that removes a record from the global structure"""
    # could use .../record/<name> in URL or as in this case as an argument .../record?name=bob
    if 'name' not in request.args:
        return "need a name to delete a record!", 400
    with RECORD_LOCK:
        if len([r for r in RECORDS if r.get('name') == request.args.get('name')]) == 0:
            return "no such record found!", 409
        RECORDS[:] = [r for r in RECORDS if r.get(      # copy all but name matches
            'name') != request.args.get('name')]
    return "OK"


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-e', '--external',
                        dest='external',
                        action='store_true',
                        help="run as external server")
    parser.add_argument('-p', '--port',
                        type=int,
                        default=5000,
                        help="port number to use")
    args = parser.parse_args()
    if args.external:
        # service can be accessed from an external PC
        app.run(debug=False, host='0.0.0.0', port=args.port)
    else:
        # available on localhost e.g. 127.0.0.1
        app.run(debug=True, port=args.port)
