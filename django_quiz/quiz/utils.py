from hashlib import sha256

from .models import UserSession


def get_user_ip(request) -> str:
    if x_forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR'):
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_user_session_hash(request) -> str:
    return sha256(get_user_ip(request).encode()).hexdigest()


def get_user_session(request) -> UserSession | None:
    users_session = UserSession.objects.filter(session=get_user_session_hash(request))
    if users_session.exists():
        return users_session.first()
