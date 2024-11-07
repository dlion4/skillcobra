from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve


class AuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            current_path = resolve(request.path_info).url_name
            print(current_path)
            if current_path not in ("login", "register", "req_password_reset_view"):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)
