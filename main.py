from flask import Flask, request, send_from_directory, make_response, abort
from functools import wraps
from schedule.schedule import add_schedule, get_schedule, get_schedule_by_day
from users.auth import do_login, load_user_info, get_root_session, use_code, register_person
from users.user import get_teachers, get_teachers_by_institute, add_teacher, update_teachers_lesson
from university.university import (get_all_institutes, get_directions, add_direction, add_institute,
                                   del_direction, del_institute, edit_institute, edit_direction,
                                   get_directions_with_groups)
from lessons.lesson import (get_lessons, get_lesson_types, add_lesson, delete_lesson, edit_lesson, add_lesson_type,
                            edit_lesson_type, delete_lesson_type)
from groups.group import (get_all_groups, get_groups_by_direction, get_subgroups_by_group, add_group, add_subgroup,
                          get_groups_by_institute_year, delete_group, delete_subgroup)
from generals.helpers import UUIDEncoder
from housing.housing import get_all_housing, add_housing, edit_housing_address
from audience.audience import get_audiences, add_audience
from exceptions.exception import ActionExceptionHandler, BeforeActionException, ExceptionsMessages
from invites.invite import generate_codes, del_code, is_active_code
from psycopg2 import errors
import json

app = Flask(__name__)
SESSIONS = {}
DEBUG_MODE = True
ROOT_SESSION = get_root_session()


def check_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
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
    """
    Дополняет входящий с фронтента json нужными параметрами
    """
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if session:
        data = SESSIONS.get(session)
        if data is None:
            data = load_user_info(session)
        if data:
            params.update(data.get_info_for_back())


def exceptions_catcher(func):
    """
    Перехватывает все наши ошибки
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except errors.UniqueViolation as ex:
            return BeforeActionException(ExceptionsMessages.NAME_DUPLICATES).get_response()
        except ActionExceptionHandler as ex:
            return ex.get_response()
    return wrapper


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('./static', path)


@app.route('/')
@app.route('/constructor')
@check_session
def main_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    return send_from_directory('./templates', 'index.html')


@app.route('/api/get_user_info', methods=["GET"])
@check_session
def get_user_info_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
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
    if params and not DEBUG_MODE:
        if params['login'] and params['password']:
            if params.get('code') and not use_code(params):
                response['error_code'] = 102
                return make_response(json.dumps(response, cls=UUIDEncoder))
            result = do_login(params['login'], params['password'])
            if result.is_authorized():
                response['success'] = True
                response.update(result.get_info_for_web())
                if result.old_session is not None and result.old_session in SESSIONS:
                    SESSIONS.pop(result.old_session)
                SESSIONS[result.session] = result
            response['error_code'] = result.error_code
            return make_response(json.dumps(response, cls=UUIDEncoder))
        else:
            return make_response(json.dumps(response, cls=UUIDEncoder))
    else:
        return make_response(json.dumps(response, cls=UUIDEncoder))


@app.route('/api/auth/register', methods=["POST"])
def register_route():
    response = {
        'success': False
    }
    params = request.get_json(force=True)
    if params and not DEBUG_MODE:
        temp = {
            'schema': params['organization'],
            'code': params['code']
        }
        if is_active_code(temp):
            if register_person(params):
                response['success'] = True
        else:
            response['error_code'] = 102
    return make_response(json.dumps(response, cls=UUIDEncoder))


@app.route('/api/get_institutes', methods=["GET"])
@check_session
def get_institutes_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_all_institutes(params), cls=UUIDEncoder))


@app.route('/api/get_directions', methods=["GET"])
@check_session
def get_directions_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_directions(params), cls=UUIDEncoder))


@app.route('/api/get_directions_with_groups', methods=["GET"])
@check_session
def get_directions_with_groups_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_directions_with_groups(params), cls=UUIDEncoder))


@app.route('/api/get_lessons', methods=["GET"])
@check_session
def get_lessons_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_lessons(params), cls=UUIDEncoder))


@app.route('/api/get_lesson_types', methods=["GET"])
@check_session
def get_lesson_types_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_lesson_types(params), cls=UUIDEncoder))


@app.route('/api/get_teachers', methods=["POST"])
@check_session
def get_teachers_route():
    params = dict(request.get_json(force=True))
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


@app.route('/api/get_groups_by_direction', methods=["GET"])
@check_session
def get_groups_by_direction_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_groups_by_direction(params), cls=UUIDEncoder))


@app.route('/api/get_groups_by_institute_year', methods=["GET"])
@check_session
def get_groups_by_institute_year_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_groups_by_institute_year(params), cls=UUIDEncoder))


@app.route('/api/get_subgroups_by_group', methods=["POST"])
@check_session
def get_subgroups_by_group_route():
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(get_subgroups_by_group(params), cls=UUIDEncoder))


@app.route('/api/add_lesson', methods=["POST"])
@check_session
@exceptions_catcher
def add_lesson_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_lesson(params), cls=UUIDEncoder))


@app.route('/api/add_lesson_type', methods=["POST"])
@check_session
@exceptions_catcher
def add_lesson_type_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_lesson_type(params), cls=UUIDEncoder))


@app.route('/api/add_direction', methods=["POST"])
@check_session
@exceptions_catcher
def add_direction_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_direction(params), cls=UUIDEncoder))


@app.route('/api/add_institute', methods=["POST"])
@check_session
@exceptions_catcher
def add_institute_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_institute(params), cls=UUIDEncoder))


@app.route('/api/add_teacher', methods=["POST"])
@check_session
@exceptions_catcher
def add_teacher_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_teacher(params), cls=UUIDEncoder))


@app.route('/api/add_teacher_to_lesson', methods=["POST"])
@check_session
def update_teachers_lesson_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(update_teachers_lesson(params), cls=UUIDEncoder))


@app.route('/api/get_housing', methods=["GET"])
@check_session
def get_housing_route():
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(get_all_housing(params), cls=UUIDEncoder))


@app.route('/api/add_housing', methods=["POST"])
@check_session
@exceptions_catcher
def add_housing_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_housing(params), cls=UUIDEncoder))


@app.route('/api/edit_housing', methods=["POST"])
@check_session
@exceptions_catcher
def edit_housing_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(edit_housing_address(params), cls=UUIDEncoder))


@app.route('/api/edit_lesson_type', methods=["POST"])
@check_session
@exceptions_catcher
def edit_lesson_type_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(edit_lesson_type(params), cls=UUIDEncoder))


@app.route('/api/get_audiences', methods=["POST"])
@check_session
def get_audiences_route():
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(get_audiences(params), cls=UUIDEncoder))


@app.route('/api/add_audience', methods=["POST"])
@check_session
@exceptions_catcher
def add_audiences_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_audience(params), cls=UUIDEncoder))


@app.route('/api/add_group', methods=["POST"])
@check_session
@exceptions_catcher
def add_group_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_group(params), cls=UUIDEncoder))


@app.route('/api/add_subgroup', methods=["POST"])
@check_session
@exceptions_catcher
def add_subgroup_route():
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_subgroup(params), cls=UUIDEncoder))


@app.route('/api/add_schedule', methods=["POST"])
@check_session
@exceptions_catcher
def add_schedule_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(add_schedule(params), cls=UUIDEncoder))


@app.route('/api/get_schedule', methods=["POST"])
@check_session
def get_schedule_route():
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(get_schedule(params), cls=UUIDEncoder))


@app.route('/api/get_schedule_by_day', methods=["POST"])
@check_session
def get_schedule_by_day_route():
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(get_schedule_by_day(params), cls=UUIDEncoder))


@app.route('/api/delete_lesson', methods=["POST"])
@check_session
def delete_lesson_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(delete_lesson(params), cls=UUIDEncoder))


@app.route('/api/delete_lesson_type', methods=["POST"])
@check_session
def delete_lesson_type_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(delete_lesson_type(params), cls=UUIDEncoder))


@app.route('/api/delete_subgroup', methods=["POST"])
@check_session
def delete_subgroup_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(delete_subgroup(params), cls=UUIDEncoder))


@app.route('/api/delete_group', methods=["POST"])
@check_session
def delete_group_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(delete_group(params), cls=UUIDEncoder))


@app.route('/api/delete_direction', methods=["POST"])
@check_session
def delete_direction_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(del_direction(params), cls=UUIDEncoder))


@app.route('/api/delete_institute', methods=["POST"])
@check_session
def delete_institute_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(del_institute(params), cls=UUIDEncoder))


@app.route('/api/edit_institute', methods=["POST"])
@check_session
def edit_institute_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(edit_institute(params), cls=UUIDEncoder))


@app.route('/api/edit_direction', methods=["POST"])
@check_session
def edit_direction_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(edit_direction(params), cls=UUIDEncoder))


@app.route('/api/edit_lesson', methods=["POST"])
@check_session
def edit_lesson_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.get_json(force=True))
    enrichment_json(params)
    return make_response(json.dumps(edit_lesson(params), cls=UUIDEncoder))


@app.route('/api/generate_invite_code', methods=['GET'])
@check_session
def generate_invite_code_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(generate_codes(params), cls=UUIDEncoder))


@app.route('/api/delete_invite_code', methods=['GET'])
@check_session
def delete_invite_code_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(del_code(params), cls=UUIDEncoder))


@app.route('/api/is_active_code', methods=['GET'])
@check_session
def is_active_code_route():
    session = ROOT_SESSION if DEBUG_MODE else request.cookies.get('_ms_AuthToken')
    if SESSIONS[session].role != 'admin':
        print(SESSIONS[session].role)
        return abort(403)
    params = dict(request.args)
    enrichment_json(params)
    return make_response(json.dumps(is_active_code(params), cls=UUIDEncoder))


if __name__ == '__main__':
    if DEBUG_MODE:
        warning_message = 'ЗАПУЩЕНО В DEBUG MODE! АВТОРИЗАЦИЯ НЕДОСТУПНА!'
        print(f'\033[93m{warning_message}\033[0m')

    app.run()
