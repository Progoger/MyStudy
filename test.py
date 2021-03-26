from flask import Flask, request, jsonify, send_from_directory
# from generals.database import SqlQuery
# from werkzeug.security import generate_password_hash, check_password_hash

# print(str(generate_password_hash('test')))
# print(check_password_hash('pbkdf2:sha256:150000$fFDjnPFl$cbc2f1add72702ad9f7c7f2582e3acb978269da637467798fa3e63707c7f2125', 'test'))


logins_passwords = {"Progoger": "ProForAll123", "Petushok": "GachaForLife123", "LukNi": "LukIamYourFather123"}
uuid_data = {"2sdfasd-asdgfdfasg-d-asgsadg":{"organisation": 'Kostroma State University', "color": '1b37d8'}}

app = Flask(__name__)


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./static', path)

@app.route('/')
def hello_world():
    return send_from_directory('./templates', 'index.html') # render_template('index.html')


@app.route('/autorize', methods=["POST"])
def autorize():
    params = request.get_json(force=True)
    if not params:
        return jsonify({"success": False})
    login = params['login']
    password = params['password']
    if login in logins_passwords.keys():
        if logins_passwords[login] == password:
            autorize_uuid = '2sdfasd-asdgfdfasg-d-asgsadg'#uuid.uuid4()
            return jsonify({"success": True, "uuid": autorize_uuid})
        else:
            return jsonify({"success": False})
    else:
        return jsonify({"success": False})


@app.route('/check_uuid', methods=["POST"])
def check_uuid():
    if request.get_json(force=True):
        uuid = request.get_json(force=True)['uuid']
        if uuid == '2sdfasd-asdgfdfasg-d-asgsadg':
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})
    else:
        return jsonify({"success": False})


@app.route('/send_data', methods=["POST"])
def send_data():
    if request.get_json(force=True):
        uuid = request.get_json(force=True)['uuid']
        if uuid in uuid_data.keys():
            return jsonify({"success": True, "result": uuid_data[uuid]})
        else:
            return jsonify({"success": False})
    else:
        return jsonify({"success": False})


if __name__ == '__main__':
    app.run()
