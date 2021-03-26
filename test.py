logins_passwords = {"Progoger": "ProForAll123", "Petushok": "GachaForLife123", "LukNi": "LukIamYourFather123"}

import flask

app = flask(__name__)

@app.route('/test', methods=["POST"])
def autorize():
    login = flask.request.form.get("login")
    password = flask.request.form.get("password")
    res = flask.request.get("https://mystudyksu.herokuapp.com/")

    if res.status_code != 200:
        return flask.jsonify({"success": False})

    data = res.json()

    if data['login'] in logins_passwords.keys():
        if logins_passwords[login] == data['password']:
            return flask.jsonify({"success": True})
        else:
            return flask.jsonify({"success": False})
    else:
        return flask.jsonify({"success": False})


if __name__ == '__main__':
    app.run()