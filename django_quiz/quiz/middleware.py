from .utils import get_user_session, get_user_session_hash
from .models import UserSession


class UserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_session = request.COOKIES.get('user_session', False)

        if not user_session:
            if not get_user_session(request):
                UserSession.objects.create(
                    session=get_user_session_hash(request),
                )

        response = self.get_response(request)

        if not user_session:
            response.set_cookie('user_session', True, max_age=315360000)

        return response
