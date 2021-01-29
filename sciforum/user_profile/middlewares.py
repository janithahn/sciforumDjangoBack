from django.utils.timezone import now
from user_profile.models import Profile


class SetLastVisitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            # Update last visit time after request finished processing.
            Profile.objects.filter(pk=request.user).update(lastAccessDate=now())

        response = self.get_response(request)

        return response