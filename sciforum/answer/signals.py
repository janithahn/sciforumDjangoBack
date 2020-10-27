from django.db.models.signals import post_save, pre_save
from notifications.signals import notify
from django.dispatch import receiver
from answer.models import Answer

@receiver(post_save, sender=Answer)
def my_handler(sender, instance, created, **kwargs):
    if created:
        #print(instance.owner)
        #notify.send(instance, recipient=instance.owner, verb='was saved')
        print('Answer created')

#post_save.connect(my_handler, sender=Answer)