from django.contrib import admin
from .models import ScheduledMail, MailAttachment, MailRecipient

# Register your models here.


@admin.register(ScheduledMail)
class MailAdmin(admin.ModelAdmin):
    pass


@admin.register(MailAttachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(MailRecipient)
class RecipientAdmin(admin.ModelAdmin):
    pass
