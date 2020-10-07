from .serializers import JWTUserSerializer, ProfileSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': JWTUserSerializer(user, context={'request': request}).data
    }