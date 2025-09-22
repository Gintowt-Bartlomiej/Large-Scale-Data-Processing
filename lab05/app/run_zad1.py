from celery_app.zad1_tasks import random_number

results = [random_number.delay() for _ in range(100)]
for i, result in enumerate(results):
    print(f'Task {i+1}: {result.get(timeout=3)}')



