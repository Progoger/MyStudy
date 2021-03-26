import flask


logins_passwords = {"Progoger": "ProForAll123", "Petushok": "GachaForLife123", "LukNi": "LukIamYourFather123"}
uuid_data = {"2sdfasd-asdgfdfasg-d-asgsadg":{"organisation": 'Костромской Государственный Университет', "color": '1b37d8'}}


app = flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello'


@app.route('/autorize', methods=["POST"])
def autorize():
    login = flask.request.form.get("login")
    password = flask.request.form.get("password")
    res = flask.request.get("https://mystudyksu.herokuapp.com/")

    if res.status_code != 200:
        return flask.jsonify({"success": False})

    data = res.json()

    if data['login'] in logins_passwords.keys():
        if logins_passwords[password] == data['password']:
            autorize_uuid = '2sdfasd-asdgfdfasg-d-asgsadg'
            return flask.jsonify({"success": True, "uuid": autorize_uuid})
        else:
            return flask.jsonify({"success": False})
    else:
        return flask.jsonify({"success": False})


@app.route('/check_uuid', methods=["POST"])
def check_uuid():
    uuid = flask.request.form.get("uuid")
    if uuid == '2sdfasd-asdgfdfasg-d-asgsadg':
        return True
    else:
        return False


@app.route('/send_data', methods=["POST"])
def send_data():
    uuid = flask.request.form.get("uuid")
    if uuid in uuid_data.keys():
        return flask.jsonify(uuid_data[uuid])


if __name__ == '__main__':
    app.run()
