from django.contrib.auth import user_logged_in, user_login_failed
from django.dispatch import receiver
from user_profile.models import Profile
import logging

error_log = logging.getLogger(__name__)

'''Signals to update login_ip and user_agent_info of the Profile model when the user receives JWT token'''

@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],

        #user_login_activity_log = Profile(login_ip=get_client_ip(request), user=user, user_agent_info=user_agent_info)
        # user_login_activity_log.save()
        Profile.objects.select_related().filter(user=user).update(login_ip=get_client_ip(request), user_agent_info=user_agent_info)

    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))

@receiver(user_login_failed)
def log_user_logged_in_failed(sender, credentials, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],

        #user_login_activity_log = Profile(login_ip=get_client_ip(request), user=credentials, user_agent_info=user_agent_info)
        # user_login_activity_log.save()
        Profile.objects.select_related().filter(user=credentials).update(login_ip=get_client_ip(request), user_agent_info=user_agent_info)


    except Exception as e:
        # log the error
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip