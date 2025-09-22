from celery import Celery

app = Celery(
    'lab5',
    broker='amqp://guest:guest@rabbitmq//',
    backend='rpc://'
)

app.autodiscover_tasks(['celery_app'])
from . import zad1_tasks
from . import zad2_tasks
from . import zad3_tasks
from . import zad4_tasks