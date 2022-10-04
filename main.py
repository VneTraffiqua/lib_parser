import requests
import urllib.parse
from pathlib import Path
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup


def download_txt_book(book_id, filename):
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


def download_book_img(img_url):
    url = f'https://tululu.org/{img_url}'
    response = requests.get(url)
    response.raise_for_status()
    url_parts = urllib.parse.urlparse(response.url)
    img_path = url_parts.path.split('/')
    img_name = img_path[-1]
    if img_name != 'nopic.gif':
        file_path = f'img/{img_name}'
        with open(file_path, 'wb') as file:
            file.write(response.content)


def get_book_params(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_img_url = soup.find(class_='bookimage').find('img')['src']
    title_tag = soup.find('body').find('h1')
    book_title, temp_str, book_author = title_tag.text.split('\xa0')
    return book_img_url, book_title, book_author


def get_book_comments(response):
    soup = BeautifulSoup(response.text, 'lxml')
    comments = soup.find_all(class_='texts')
    comments_texts = []
    for comment in comments:
        comment_text = comment.find('span')
        comments_texts.append(comment_text.text)
    return comments_texts


def get_book_genre(response):
    soup = BeautifulSoup(response.text, 'lxml')
    genres_soup = soup.find_all('span', class_='d_book')
    for item in genres_soup:
        genres_with_tags = item.find_all('a')
        genres = []
    for genre in genres_with_tags:
        genres.append(genre.text)
    return genres


def parse_book_page(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    if response.url == url:
        book_img_url, book_title, book_author = get_book_params(response)
        # download_txt_book(book_id, book_title)
        # download_book_img(book_img_url)
        print('Книга:', book_title)
        print('Автор:', book_author)
        print('Жанр:', get_book_genre(response))
        print('Комментарии', get_book_comments(response))


if __name__ == '__main__':
    # Отключенные создания папок пока нет сохранения книг и обложек
    # Path('./books').mkdir(parents=True, exist_ok=True)
    # Path('./img').mkdir(parents=True, exist_ok=True)
    for book_id in range(5, 11):
        parse_book_page(book_id)
