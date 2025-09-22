import sys
from celery_app.zad3_tasks import append_to_poem

word = sys.argv[1]
result = append_to_poem.delay(word)
print(result.get(timeout=10))
