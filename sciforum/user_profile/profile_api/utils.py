from .serializers import JWTUserSerializer
from firebase_admin import auth


def jwt_response_payload_handler(token, user=None, request=None):

    firebase_token = auth.create_custom_token(user.username)

    return {
        'token': token,
        'user': JWTUserSerializer(user, context={'request': request}).data,
        'firebase_token': firebase_token
    }


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip