from celery_app.zad4_tasks import task_pipeline

if __name__ == "__main__":
    result = task_pipeline()
    final_result = result.get(timeout=60)

    print("Wyniki potoku:")
    for i, r in enumerate(final_result, 1):
        print(f"{i}. {r}")
