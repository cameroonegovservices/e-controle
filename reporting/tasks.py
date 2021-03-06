import logging
from datetime import timedelta

from django.utils import timezone

from actstream import action
from celery import task
from celery.utils.log import get_task_logger

from control.models import Control, ResponseFile
from utils.email import send_email


logger = get_task_logger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def get_files(control):
    latest_email_sent = control.actor_actions.filter(verb='sent-files-report').first()
    if latest_email_sent:
        date_cutoff = latest_email_sent.timestamp
    else:
        date_cutoff = timezone.now() - timedelta(hours=24)
    logger.info(f"Looking for files uploaded after this timestamp: {date_cutoff}")
    files = ResponseFile.objects.filter(
        question__theme__questionnaire__control=control,
        created__gt=date_cutoff,
    )
    logger.info(f'Number of files: {len(files)}')
    return files


@task
def send_files_report():
    html_template = 'reporting/email/files_report.html'
    text_template = 'reporting/email/files_report.txt'
    for control in Control.objects.all():
        logger.info(f'Processing control: {control}')
        subject = f'{control.reference_code} - de nouveaux documents déposés !'
        logger.debug(f"Email subject: {subject}")
        files = get_files(control)
        if not files:
            continue
        recipients = control.user_profiles.filter(send_files_report=True)
        recipient_list = recipients.values_list('user__email', flat=True)
        logger.info(f'Recipients: {recipient_list}')
        if not recipient_list:
            continue
        context = {'files': files}
        number_of_sent_email = send_email(
            subject=subject,
            text_template=text_template,
            html_template=html_template,
            recipient_list=recipient_list,
            extra_context=context,
        )
        logger.info(f"Sent {number_of_sent_email} emails")
        number_of_recipients = len(recipient_list)
        if number_of_sent_email != number_of_recipients:
            logger.warning(
                "There was {number_of_recipients} recipients, "
                "but {number_of_sent_email} email(s) sent.")
        logger.info(f'Email sent for {control}')
        action.send(sender=control, verb='sent-files-report')
