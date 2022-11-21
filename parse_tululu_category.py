import os.path
import requests
import argparse
import re
import time
import json
import sys
from bs4 import BeautifulSoup
import urllib.parse
from urllib.error import URLError
from pathlib import Path
from parse_tululu import download_book_img, download_txt_book, \
    check_for_redirect, get_book_params


def get_books_url(soup):
    books_selector = '#content .bookimage a'
    all_books_on_page = soup.select(books_selector)
    all_books_path = [book['href'] for book in all_books_on_page]
    return all_books_path


def main():
    parser = argparse.ArgumentParser(
        description='Enter start page and optional param, for parsing books'
    )
    parser.add_argument(
        '--start_page',
        type=int,
        help='start page number',
        default=1
    )
    parser.add_argument(
        '--last_page',
        type=int,
        help='end page number',
        default=None
    )
    parser.add_argument(
        '--dest_folder',
        type=str,
        help='path to the dir with parsing results: pictures, books, JSON',
        default='.'
    )
    parser.add_argument(
        '--json_path',
        type=str,
        help='your path to *.json file with results',
        default='./'
    )
    parser.add_argument(
        '--skip_imgs',
        action='store_true',
        help='if True, do not download pictures',
        default=False
    )
    parser.add_argument(
        '--skip_txt',
        action='store_true',
        help='if True, do not download books',
        default=False
    )
    args = parser.parse_args()

    Path(f'{args.dest_folder}/books').mkdir(parents=True, exist_ok=True)
    Path(f'{args.dest_folder}/img').mkdir(parents=True, exist_ok=True)
    all_books_params = []
    page = args.start_page
    if args.last_page:
        last_page = args.last_page
    else:
        last_page = page

    while page <= last_page:
        try:
            url = f'https://tululu.org/l55/{page}'
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
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
                    if not args.skip_imgs:
                        img_src = download_book_img(book_url, book_img_url)
                    book_id = re.sub(r"[^\d\.]", "", book_path)
                    if not args.skip_txt:
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
                page += 1
        except URLError:
            page += 1
            continue
        except requests.exceptions.HTTPError:
            print('HTTP error...')
            page += 1
            continue
        except requests.exceptions.ConnectionError:
            print('Failed connection..', file=sys.stderr)
            time.sleep(3)
            continue
        books_json = json.dumps(all_books_params, ensure_ascii=False)
        with open(f'{args.json_path}books.json', 'w') as file:
            file.write(books_json)


if __name__ == '__main__':
    main()
