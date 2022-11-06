from celery import Celery
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from user_profile.models import Profile, UserInterests
from post.models import Post
from datetime import date, timedelta

app = Celery()

'''@task(name='summary')
def send_import_summary():
    #Magic happens here ...
    pass
# or'''

auto_mail_from = 'from@mail.com'
if hasattr(settings, 'AUTO_MAIL_FROM'):
    auto_mail_from = settings.AUTO_MAIL_FROM


today = date.today()
yesterday = today - timedelta(days=1)


plaintext = get_template('daily_notification.txt')
html = get_template('daily_notification.html')


# @shared_task
@app.task()
def send_moderator_daily_notification():
    queryset = Profile.objects.filter(userRole='MODERATOR')
    recipients = [query.user for query in queryset]
    print(recipients)

    for recipient in recipients:
        interests = [interest.interest for interest in UserInterests.objects.filter(user=recipient)]
        posts_list = [{'title': post.title, 'url': settings.URL_FRONT + 'questions/' + str(post.id)} for post in Post.objects.filter(label__in=interests) if post.created_at.date() == yesterday]

        if len(posts_list) != 0:
            ctx = {
                'username': recipient.username,
                'base_url': settings.URL_FRONT,
                'posts': posts_list
            }

            # d = Context({'username': recipient.username, 'base_url': settings.URL_FRONT, 'posts': posts_list})
            subject, from_email, to = 'sciForum Daily Updates', auto_mail_from, recipient.email
            text_content = plaintext.render(ctx)
            html_content = html.render(ctx)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    '''message = 'testing celery task'
    recipient_list = ('janithahn@gmail.com', )
    mail_msg = EmailMessage(
        subject='sciForum Daily Updates',
        body=message,
        from_email=auto_mail_from,
        to=recipient_list,
    )
    mail_msg.content_subtype = 'html'
    mail_msg.send()'''

