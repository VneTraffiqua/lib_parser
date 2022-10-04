import requests
import urllib.parse
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


def save_txt_book(book_id, filename):
    url = 'https://tululu.org/txt.php'
    params = {
        'id': book_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    url_parts = urllib.parse.urlparse(response.url)
    if url_parts.query:
        file_path = f'books/{book_id}. {sanitize_filename(filename)}.txt'
        with open(file_path, 'wb') as file:
            file.write(response.content)


def get_book_params(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_img_url = soup.find(class_='bookimage').find('img')['src']
    title_tag = soup.find('body').find('h1')
    book_title, temp_str, book_author = title_tag.text.split('\xa0')
    return book_img_url, book_title, book_author


if __name__ == '__main__':
    Path('./books').mkdir(parents=True, exist_ok=True)
    for book_id in range(1, 11):
        url = f'https://tululu.org/b{book_id}/'
        response = requests.get(url)
        response.raise_for_status()
        if response.url == url:
            book_img_url, book_title, book_author = get_book_params(response)
            save_txt_book(book_id, book_title)
            print(book_title)
            print(book_author)
            print(book_img_url)
        # save_txt_book(book_id, book_title)
