from .serializers import JWTUserSerializer
from firebase_admin import auth
from django.contrib.auth.models import User
from allauth.account.admin import EmailAddress
from notifications.signals import notify
from notifications.models import Notification


def jwt_response_payload_handler(token, user=None, request=None):

    # email verify notification
    email_verified = EmailAddress.objects.get(user=user).verified
    from_user = User.objects.get(username='admin')
    to_user = user
    message = 'Your account has not been verified yet. Please check your email or go to account settings and verify your account.'
    if not email_verified:
        try:
            notification = to_user.notifications.filter(actor_object_id=from_user.id, recipient=user, description='email_verification')
            notification.delete()
            notify.send(sender=from_user, recipient=to_user, verb=message, description='email_verification')
        except Exception as excep:
            print(excep)

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