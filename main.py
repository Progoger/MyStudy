from flask import Flask, request, send_from_directory, make_response
from functools import wraps
from users.auth import do_login, load_user_info
from users.user import get_teachers, get_teachers_by_institute, add_teacher
from university.university import get_all_institutes, get_directions, add_direction, add_institute
from lessons.lesson import get_lessons, add_lesson
from groups.group import get_all_groups
from generals.helpers import UUIDEncoder
import json

app = Flask(__name__)
SESSIONS = {}
ROOT_SESSION = '46936881-b926-4321-a583-35d7fe1fece9'


def check_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = ROOT_SESSION # request.cookies.get('_ms_AuthToken')
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


def enrichment_json(params):
    session = ROOT_SESSION #request.cookies.get('_ms_AuthToken')
    if session:
        data = SESSIONS.get(session)
        if data is None:
            data = load_user_info(session)
        if data:
            params.update(data.get_info_for_back())


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('./static', path)


@app.route('/')
@app.route('/constructor')
def main_route():
    return send_from_directory('./templates', 'index.html')


@app.route('/api/get_user_info', methods=["GET"])
@check_session
def get_user_info_route():
    session = ROOT_SESSION#request.cookies.get('_ms_AuthToken')
    response = {
        'success': True
    }
    response.update(SESSIONS[session].get_info_for_web())
    return make_response(json.dumps(response, cls=UUIDEncoder))


@app.route('/api/auth/login', methods=["POST"])
def login_route():
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
            return make_response(json.dumps(response, cls=UUIDEncoder))
        else:
            return make_response(json.dumps(response, cls=UUIDEncoder))
    else:
        return make_response(json.dumps(response, cls=UUIDEncoder))


@app.route('/api/get_institutes', methods=["GET"])
@check_session
def get_institutes_route():
    params = {}
    enrichment_json(params)
    return make_response(json.dumps(get_all_institutes(params), cls=UUIDEncoder))


@app.route('/api/get_directions', methods=["GET"])
@check_session
def get_directions_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_directions(params), cls=UUIDEncoder))


@app.route('/api/get_lessons', methods=["GET"])
@check_session
def get_lessons_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_lessons(params), cls=UUIDEncoder))


@app.route('/api/get_teachers', methods=["GET"])
@check_session
def get_teachers_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_teachers(params), cls=UUIDEncoder))


@app.route('/api/get_teachers_by_institute', methods=["GET"])
@check_session
def get_teachers_by_institute_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_teachers_by_institute(params), cls=UUIDEncoder))


@app.route('/api/get_all_groups', methods=["GET"])
@check_session
def get_all_groups_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_all_groups(params), cls=UUIDEncoder))


@app.route('/api/add_lesson', methods=["POST"])
@check_session
def add_lesson_route():
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_lesson(params), cls=UUIDEncoder))


@app.route('/api/add_direction', methods=["POST"])
@check_session
def add_direction_route():
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_direction(params), cls=UUIDEncoder))


@app.route('/api/add_institute', methods=["POST"])
@check_session
def add_institute_route():
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_institute(params), cls=UUIDEncoder))


@app.route('/api/add_teacher', methods=["POST"])
@check_session
def add_teacher_route():
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_teacher(params), cls=UUIDEncoder))


if __name__ == '__main__':
    app.run()
