import os
import datetime
from datetime import date

from django.db import models
from django.utils import timezone
from django.core.mail import EmailMessage

from django.conf import settings

auto_mail_from = 'from@mail.com'
if hasattr(settings, 'AUTO_MAIL_FROM'):
    auto_mail_from = settings.AUTO_MAIL_FROM

mail_dir = os.path.join(settings.BASE_DIR, 'mail_templates/')


class MailAttachment(models.Model):
    attachment_file = models.FileField()
    attached_to = models.ForeignKey('ScheduledMail', related_name='attachments', on_delete=models.CASCADE)

    def __str__(self): 
        return '%s (%s)' % (self.attachment_file.filename, self.attached_to.subject)


class MailRecipient(models.Model):
    mail_address = models.CharField(max_length=40)

    def __str__(self):
        return self.mail_address


class ScheduledMail(models.Model):
    subject = models.CharField(max_length=40)
    template = models.FileField()
    send_on = models.DateTimeField(default=timezone.now())
    recipients_list = models.ManyToManyField(MailRecipient, related_name='mail_list')

    def __str__(self):
        return self.subject

    @classmethod
    def get_today_mail(cls):
        today = date.today()
        return cls.objects.filter(send_on__year=today.year, send_on__month=today.month, send_on__day=today.day)

    def send_scheduled_mail(self):
        message = self.template.read().decode('utf-8')
        recipient_list = list(self.recipients_list.values_list('mail_address', flat=True))
        mail_msg = EmailMessage(
            subject=self.subject,
            body=message,
            from_email=auto_mail_from,
            to=recipient_list,
        )
        mail_msg.content_subtype = 'html'
        mail_msg.send()
