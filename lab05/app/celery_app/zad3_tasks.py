from celery_app import app
import threading

lock = threading.Lock()
poem_file = "poemat.txt"

@app.task
def append_to_poem(word):
    with lock:
        try:
            with open(poem_file, "r+", encoding="utf-8") as f:
                content = f.read().strip()
                words = content.split()
                words.append(word)

                f.seek(0)
                f.truncate()
                for i in range(0, len(words), 5):
                    f.write(" ".join(words[i:i+5]) + "\n")

        except FileNotFoundError:
            with open(poem_file, "w", encoding="utf-8") as f:
                f.write(word + "\n")

        return f"Dodano słowo: {word}"