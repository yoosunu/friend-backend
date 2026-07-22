from rest_framework.views import exception_handler


def jwt_ignore_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 401:
        if "token" in str(exc).lower() and "expired" in str(exc).lower():
            return response

    return response
