import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import json
from more_itertools import chunked
from pathlib import Path


def on_reload():
    with open('books.json', 'r') as file:
        books_json = file.read()
    books = json.loads(books_json)
    env = Environment(
        loader=FileSystemLoader('./'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    os.makedirs('./pages', exist_ok=True)
    books_pages = list(chunked(books, 20))
    for num, books_on_page in enumerate(books_pages, 1):
        grouped_books = list(chunked(books_on_page, 2))
        template = env.get_template('template.html')
        rendered_page = template.render(
            number_of_page=num,
            grouped_books=grouped_books,
            count_pages=len(books_pages)
        )
        with open(
                Path.cwd() / 'pages' / f'index{num}.html',
                'w',
                encoding="utf8",
        ) as file:
            file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('./template.html', on_reload)
    server.serve(root='.', default_filename='pages/index1.html')

    # server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    # server.serve_forever()


if __name__ == '__main__':
    main()
