from . import app
import requests
from bs4 import BeautifulSoup

@app.task
def get_nth_word(n):
    try:
        response = requests.get('https://pl.wikipedia.org/wiki/Special:Random', timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', {'id': 'mw-content-text'})

        words = content.get_text(separator=' ', strip=True).split() if content else []

        if not words:
            return "słowo"

        if n < 1 or n > len(words):
            word = words[-1]
        else:
            word = words[n - 1]

        clean_word = word.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        return clean_word

    except:
        return "słowo"



