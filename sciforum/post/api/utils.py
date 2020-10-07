from .serializers import JWTUserSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': JWTUserSerializer(user, context={'request': request}).data
    }