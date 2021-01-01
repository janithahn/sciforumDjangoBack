from django.contrib.auth import user_logged_in, user_login_failed
from django.dispatch import receiver
from user_profile.models import Profile
from allauth.account.signals import user_signed_up, user_logged_in
from urllib.request import urlretrieve
import io
from PIL import Image
import copy
import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    font_end_url = 'http://localhost:3000/users/profile/password_reset/confirm/'

    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': font_end_url + "{}".format(
            reset_password_token.key)
    }

    ''''
    reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    '''

    # render email text
    email_html_message = render_to_string('user_profile/reset_password.html', context)
    email_plaintext_message = render_to_string('user_profile/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="sciForum"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@sciforum.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


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

        # user_login_activity_log = Profile(login_ip=get_client_ip(request), user=credentials, user_agent_info=user_agent_info)
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


'''@receiver(user_signed_up)
def social_login_profilepic(sociallogin, user, **kwargs):

    if sociallogin:
        # Extract first / last names from social nets and store on User record
        #verified = sociallogin.account.extra_data['verified_email']
        picture_url = sociallogin.account.extra_data['picture']

    image, header = urlretrieve(picture_url, 'picture.jpg')
    #image = download_image(picture_url)

    profile = Profile.objects.get(user=user)
    profile.profileImg.save(os.path.basename(picture_url), File(open(image, 'rb')))
    profile.save(update_fields=('profileImg', ))

    print(profile.profileImg.url)'''


def download_image(url):
    """Downloads an image and makes sure it's verified.

    Returns a PIL Image if the image is valid, otherwise raises an exception.
    """
    image, header = urlretrieve(url)
    img_temp = io.StringIO()
    image.save(img_temp, 'jpg')
    img = Image.open(img_temp) # Creates an instance of PIL Image class - PIL does the verification of file
    img_copy = copy.copy(img_temp) # Verify the copied image, not original - verification requires you to open the image again after verification, but since we don't have the file saved yet we won't be able to. This is because once we read() urllib2.urlopen we can't access the response again without remaking the request (i.e. downloading the image again). Rather than do that, we duplicate the PIL Image in memory.
    if valid_img(img_copy):
        return img
    else:
        # Maybe this is not the best error handling...you might want to just provide a path to a generic image instead
        raise Exception('An invalid image was detected when attempting to save a Product!')


def valid_img(img):
    """Verifies that an instance of a PIL Image Class is actually an image and returns either True or False."""
    type = img.format
    if type in ('GIF', 'JPEG', 'JPG', 'PNG'):
        try:
            img.verify()
            return True
        except:
            return False
    else: return False