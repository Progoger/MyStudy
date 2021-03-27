from flask import Flask, request, send_from_directory, make_response
from users.auth import do_login, load_user_info
from functools import wraps

app = Flask(__name__)
SESSIONS = {}


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('./static', path)


@app.route('/')
@app.route('/constructor')
def hello_world():
    return send_from_directory('./templates', 'index.html')


@app.route('/authorize', methods=["POST"])
@app.route('/login', methods=["GET"])
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
                response.update(result.get_info_for_web())
                if result.old_session is not None and result.old_session in SESSIONS:
                    SESSIONS.pop(result.old_session)
                SESSIONS[result.session] = result
            return make_response(response)
        else:
            return make_response(response)
    else:
        return make_response(response)


def check_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = request.cookies.get('_ms_AuthToken')
        if session:
            user = load_user_info(session)
            if user.is_authorized():
                SESSIONS[user.session] = user
                return func(*args, **kwargs)
            else:
                if user.session in SESSIONS:
                    SESSIONS.pop(user.session)
        resp = make_response({'success': False}, 401)
        resp.set_cookie('_ms_AuthToken', '', expires=0)
        return resp
    return wrapper


@app.route('/check_uuid', methods=["POST"])
@app.route('/get_user_info', methods=["GET"])
@check_session
def get_user_info():
    session = request.cookies.get('_ms_AuthToken')
    response = {
        'success': True
    }
    response.update(SESSIONS[session].get_info_for_web())
    return make_response(response)


if __name__ == '__main__':
    app.run()
