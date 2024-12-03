from django.core.exceptions import PermissionDenied


class JSXMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.endswith(".jsx"):
            response["Content-Type"] = "text/javascript"
        return response


class TutorRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.role != "instructor" and request.path == "/instructor/recruitment/":  # noqa: E501
            msg = (
                "You do not have permission to access this page. <br />"
                "Possible your are registered as a <strong>student</strong> and not a tutor. <br />"  # noqa: E501
                "This page is only for <strong>tutors</strong>. If you think this is a mistake please feel free to reach out to us"  # noqa: E501
            )
            raise PermissionDenied(msg)
        return self.get_response(request)
