import requests
import urllib.parse
from pathlib import Path


def save_txt_book(url, book_id):
    response = requests.get(url)
    response.raise_for_status()
    url_parts = urllib.parse.urlparse(response.url)
    #print(url_parts)
    if url_parts.query:
        filename = f'books/{book_id}.txt'
        with open(filename, 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    Path('./books').mkdir(parents=True, exist_ok=True)
    for book_id in range(1, 11):
        url = f'https://tululu.org/txt.php?id={book_id}'
        save_txt_book(url, book_id)
