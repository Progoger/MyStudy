from functools import wraps
from users.auth import load_user_info


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


def enrichment_json(params):
    session = request.cookies.get('_ms_AuthToken')
    if session:
        data = SESSIONS.get(session)
        if data is None:
            data = load_user_info(session)
        if data:
            params.update(data.get_info_for_back())