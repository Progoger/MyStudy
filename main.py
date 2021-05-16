from flask import Flask, request, send_from_directory, make_response
from generals.validate import check_session, enrichment_json
from users.auth import do_login
from university.university import get_all_universities, get_all_directions

app = Flask(__name__)
SESSIONS = {}


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('./static', path)


@app.route('/')
@app.route('/constructor')
def hello_world():
    return send_from_directory('./templates', 'index.html')


@app.route('/get_user_info', methods=["GET"])
@check_session
def get_user_info():
    session = request.cookies.get('_ms_AuthToken')
    response = {
        'success': True
    }
    response.update(SESSIONS[session].get_info_for_web())
    return make_response(response)


@app.route('/api/auth/login', methods=["POST"])
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


@app.route('/api/get_universities', methods=["GET"])
@check_session
def get_univers():
    response = {
        'success': True
    }
    params = {}
    enrichment_json(params)
    response.update(get_all_universities(params))
    return make_response(response)


@app.route('/api/get_directions', methods=["GET"])
@check_session
def get_directs():
    response = {
        'success': True
    }
    params = {}
    enrichment_json(params)
    response.update(get_all_directions(params))
    return make_response(response)


if __name__ == '__main__':
    app.run()
