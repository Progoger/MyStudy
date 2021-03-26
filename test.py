import flask


logins_passwords = {"Progoger": "ProForAll123", "Petushok": "GachaForLife123", "LukNi": "LukIamYourFather123"}
uuid_data = {"2sdfasd-asdgfdfasg-d-asgsadg":{"organisation": 'Костромской Государственный Университет', "color": '1b37d8'}}

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello'


@app.route('/check', methods=["POST"])
def check():
    return flask.Request.get_json()

@app.route('/autorize', methods=["POST"])
def autorize(params):
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
def check_uuid(uuid):
    if uuid == '2sdfasd-asdgfdfasg-d-asgsadg':
        return True
    else:
        return False


@app.route('/send_data', methods=["POST"])
def send_data(uuid):
    if uuid in uuid_data.keys():
        return flask.jsonify(uuid_data[uuid])


if __name__ == '__main__':
    app.run()
