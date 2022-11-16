import requests
import urllib.parse
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
import argparse
from urllib.error import URLError
from pathlib import Path
import time
import sys


def download_txt_book(book_id, filename):
    url = 'https://tululu.org/txt.php'
    params = {
        'id': book_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    book_name = sanitize_filename(filename)
    file_path = Path.cwd() / f'books/{book_id}. {book_name}.txt'
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path


def download_book_img(url, img_url):
    url = urllib.parse.urljoin(url, img_url)
    response = requests.get(url)
    response.raise_for_status()
    url_parts = urllib.parse.urlparse(response.url)
    img_path = url_parts.path.split('/')
    img_name = img_path[-1]
    if img_name == 'nopic.gif':
        return Path.cwd() / 'img' / 'nopic.gif'
    file_path = Path.cwd() / f'img/{img_name}'
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path


def get_book_params(soup):
    book_img_selector = '.bookimage img'
    book_img_url = soup.select_one(book_img_selector)['src']
    title_selector = 'body h1'
    title_tag = soup.select_one(title_selector)
    book_title, temp_str, book_author = title_tag.text.split('\xa0')
    genres_selector = 'span.d_book a'
    genres_with_tags = soup.select(genres_selector)
    genres = []
    for genre in genres_with_tags:
        genres.append(genre.text)
    comments_selector = '.texts span'
    comments = soup.select(comments_selector)
    comments_texts = []
    for comment in comments:
        comments_texts.append(comment.text)
    return book_img_url, book_title, book_author, genres, comments_texts


def check_for_redirect(response):
    if response.history:
        raise URLError('Book not found')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Enter id_from and id_to, for parsing books'
    )
    parser.add_argument('id_from', type=int, help='initial id')
    parser.add_argument('id_to', type=int, help='final id')
    args = parser.parse_args()

    Path('./books').mkdir(parents=True, exist_ok=True)
    Path('./img').mkdir(parents=True, exist_ok=True)
    book_id, book_id_to = args.id_from, args.id_to
    while book_id <= book_id_to:
        try:
            url = f'https://tululu.org/b{book_id}/'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            book_img_url, book_title, book_author, \
                genres, comments_texts = get_book_params(soup)
            print('Книга:', book_title)
            print('Автор:', book_author)
            print('Жанр:', genres)
            print('Комментарии:', comments_texts)
            print()
            download_book_img(url, book_img_url)
            download_txt_book(book_id, book_title)
            book_id += 1
        except URLError:
            book_id += 1
            continue
        except requests.exceptions.HTTPError:
            book_id += 1
            print('HTTP error...')
            continue
        except requests.exceptions.ConnectionError:
            print('Failed connection..', file=sys.stderr)
            time.sleep(3)
            continue
