import flask


logins_passwords = {"Progoger": "ProForAll123", "Petushok": "GachaForLife123", "LukNi": "LukIamYourFather123"}
uuid_data = {"2sdfasd-asdgfdfasg-d-asgsadg":{"organisation": 'Костромской Государственный Университет'.encode('utf-8'), "color": '1b37d8'}}

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello'


@app.route('/autorize', methods=["POST"])
def autorize():
    params = flask.request.get_json(force=True)
    if not params:
        return flask.jsonify({"success": False})
    login = params['login']
    password = params['password']
    if login in logins_passwords.keys():
        if logins_passwords[login] == password:
            autorize_uuid = '2sdfasd-asdgfdfasg-d-asgsadg'#uuid.uuid4()
            return flask.jsonify({"success": True, "uuid": autorize_uuid})
        else:
            return flask.jsonify({"success": False})
    else:
        return flask.jsonify({"success": False})


@app.route('/check_uuid', methods=["POST"])
def check_uuid():
    if flask.request.get_json(force=True):
        uuid = flask.request.get_json(force=True)['uuid']
        if uuid == '2sdfasd-asdgfdfasg-d-asgsadg':
            return flask.jsonify({"success": True})
        else:
            return flask.jsonify({"success": False})
    else:
        return flask.jsonify({"success": False})


@app.route('/send_data', methods=["POST"])
def send_data():
    if flask.request.get_json(force=True):
        uuid = flask.request.get_json(force=True)['uuid']
        if uuid in uuid_data.keys():
            return flask.jsonify({"success": True, "result": uuid_data[uuid]})
        else:
            return flask.jsonify({"success": False})
    else:
        return flask.jsonify({"success": False})



if __name__ == '__main__':
    app.run()
