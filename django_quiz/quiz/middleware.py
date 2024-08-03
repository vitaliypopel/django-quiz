from .utils import get_user_session, get_user_session_hash
from .models import UserSession


class UserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not get_user_session(request):
            UserSession.objects.create(
                session=get_user_session_hash(request),
            )

        return self.get_response(request)
