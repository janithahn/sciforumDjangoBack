from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.utils.encoding import force_str


class AccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        context['activate_url'] = settings.URL_FRONT + 'verify-email/' + context['key']
        msg = self.render_mail(template_prefix, email, context)
        msg.send()

    def format_email_subject(self, subject):
        prefix = "[{name}] ".format(name=settings.URL_FRONT_NAME)
        return prefix + force_str(subject)
