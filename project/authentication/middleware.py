from django.shortcuts import redirect, reverse


class RestrictAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_urls = (
            reverse('login'),
            reverse('registration'),
        )

        if request.user.is_authenticated and request.path in auth_urls:
            return redirect(reverse('quiz:dashboard'))

        return self.get_response(request)
