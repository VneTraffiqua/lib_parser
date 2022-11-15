import requests
from bs4 import BeautifulSoup
import urllib.parse


def get_book_url(scheme, netloc, soup):
    path = soup.find(id='content').find(class_='bookimage').find('a')['href']
    book_url = urllib.parse.urljoin(f'{scheme}://{netloc}', path)
    print(book_url)

def main():
    url = 'https://tululu.org/l55/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    get_book_url(
        urllib.parse.urlparse(url).scheme,
        urllib.parse.urlparse(url).netloc,
        soup
    )


if __name__ == '__main__':
    main()
