import datetime

from django.core.management import BaseCommand

from mail_app.models import ScheduledMail


class Command(BaseCommand):
    help = 'Sends an email to any user for which registered as MODERATOR.'

    def handle(self, *args, **options):
        today_mail = ScheduledMail.get_today_mail()
        print('handling command')
        for mail_message in today_mail:
            mail_message.send_scheduled_mail()
