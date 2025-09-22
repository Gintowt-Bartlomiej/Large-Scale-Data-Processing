from celery import group, chain
from .zad1_tasks import random_number
from .zad2_tasks import get_nth_word
from .zad3_tasks import append_to_poem

def task_pipeline():
    pipeline_group = group(
        chain(random_number.s(), get_nth_word.s(), append_to_poem.s())
        for _ in range(100)
    )
    return pipeline_group()
