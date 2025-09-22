import sys
from celery_app.zad2_tasks import get_nth_word

n = int(sys.argv[1])
result = get_nth_word.delay(n)
print(f"{n} słowo artykułu to: {result.get(timeout=10)}")


