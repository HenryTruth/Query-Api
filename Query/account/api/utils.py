import datetime
from django.conf import settings
from django.utils import timezone
from rest_framework_jwt.settings import api_settings

expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token':token,
        'user': user.username,
        'expires': timezone.now() + expire_delta - datetime.timedelta(seconds=200)
    }



from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response