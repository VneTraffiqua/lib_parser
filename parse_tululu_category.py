import os.path
import requests
import re
import time
import json
from bs4 import BeautifulSoup
import urllib.parse
from urllib.error import URLError

from pathlib import Path
from parse_tululu import download_book_img, download_txt_book, \
    check_for_redirect, get_book_params


def get_books_url(soup):
    all_books_path = []
    all_book_on_page = soup.find(id='content').find_all(class_='bookimage')
    for book in all_book_on_page:
        path = book.find('a')['href']
        all_books_path.append(path)
    return all_books_path


def main():
    Path('./books').mkdir(parents=True, exist_ok=True)
    Path('./img').mkdir(parents=True, exist_ok=True)
    all_books_params = []
    for page in range(1, 2):
        url = f'https://tululu.org/l55/{page}'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        all_books_path = get_books_url(soup)
        for book_path in all_books_path:
            try:
                book_url = urllib.parse.urljoin(
                    'https://tululu.org/',
                    book_path
                )
                response = requests.get(book_url)
                response.raise_for_status()
                check_for_redirect(response)
                soup = BeautifulSoup(response.text, 'lxml')
                book_img_url, book_title, book_author, \
                    genres, comments_texts = get_book_params(soup)
                img_src = download_book_img(book_url, book_img_url)
                book_id = re.sub(r"[^\d\.]", "", book_path)
                book_path = download_txt_book(book_id, book_title)

                book_params = {
                    'title': book_title,
                    'Author': book_author,
                    'img_src': os.path.relpath(img_src),
                    'book_path': os.path.relpath(book_path),
                    'genres': genres,
                    'comments': comments_texts,
                }
                all_books_params.append(book_params)
            except URLError:
                continue
            except requests.exceptions.HTTPError:
                print('HTTP error...')
                continue
            except requests.exceptions.ConnectionError:
                time.sleep(3)
                continue
    books_json = json.dumps(all_books_params, ensure_ascii=False)
    with open('books.json', 'w') as file:
        file.write(books_json)

if __name__ == '__main__':
    main()
