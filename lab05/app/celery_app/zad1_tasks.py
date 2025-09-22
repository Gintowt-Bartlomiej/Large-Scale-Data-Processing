from . import app
import random

@app.task
def random_number():
    return random.randint(0, 200)




