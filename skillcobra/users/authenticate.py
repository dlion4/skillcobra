from django.contrib.auth.backends import ModelBackend


class AuthenticateBackend(ModelBackend):
    def authenticate(self, request, username = ..., password = ..., **kwargs):
        
        return super().authenticate(request, username, password, **kwargs)

