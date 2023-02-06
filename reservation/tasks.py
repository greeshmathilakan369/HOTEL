from email import message
from logging import Logger

from celery import shared_task
from Hotel_final import settings
from django.core.mail import send_mail
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)




# @shared_task
# def sleepy(duration):
#     sleep(duration)
#     return None

@shared_task
def send_mail_task(email,msg1):
    logger.info("inside send mail task")
    send_mail(
            subject='Reservation Details',
            message=msg1,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently = False,
            )
    print("mail send")
    return "Done"


@shared_task
def send_mail_cancel_task(email,msg2):
    logger.info("inside send mail task")
    send_mail(
            subject='Reservation Details',
            message=msg2,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently = False,
            )
    print("mail send")
    return "Done"
    