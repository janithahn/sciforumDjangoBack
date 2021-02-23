from celery import shared_task


'''@task(name='summary')
def send_import_summary():
    #Magic happens here ...
    pass
# or'''


@shared_task
def send_notification():
     print('Running celery task')