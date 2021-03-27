from flask import Flask, request, send_from_directory, make_response
from users.auth import do_login

app = Flask(__name__)
SESSIONS = {}


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('./static', path)


@app.route('/')
@app.route('/constructor')
def hello_world():
    return send_from_directory('./templates', 'index.html')


@app.route('/login', methods=["POST"])
def login():
    response = {
        'success': False,
        'session': None
    }
    params = request.get_json(force=True)
    if params:
        if params['login'] and params['password']:
            result = do_login(params['login'], params['password'])
            if result.is_authorized():
                response['success'] = True
                response.update(result.get_info())
                if result.old_session is not None and result.old_session in SESSIONS:
                    SESSIONS.pop(result.old_session)
                SESSIONS[result.session] = result
            return make_response(response)
        else:
            return make_response(response)
    else:
        return make_response(response)


if __name__ == '__main__':
    app.run()
