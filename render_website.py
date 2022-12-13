from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
import json
from more_itertools import chunked

def on_reload():
    with open('books.json', 'r') as file:
        books_json = file.read()
    books = json.loads(books_json)
    env = Environment(
        loader=FileSystemLoader('./'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    grouped_books = list(chunked(books, 2))
    template = env.get_template('template.html')
    rendered_page = template.render(
        grouped_books=grouped_books
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('./template.html', on_reload)
    server.serve(root='.')

    # server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    # server.serve_forever()


if __name__ == '__main__':
    main()
