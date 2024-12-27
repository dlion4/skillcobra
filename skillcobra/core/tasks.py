import logging

from celery import shared_task

logger = logging.Logger(__file__)

@shared_task
def process_runtime_counter():
    counter = 0
    counter +=1
    logger.info("process_runtime_counter: %d" % counter)  # noqa: G002
