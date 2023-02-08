import requests
from bs4 import BeautifulSoup


def code_source(url):
    """
    :return: code source from url
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    html = requests.get(url, headers=headers)
    return html.text


def retrieve_links(html):
    soup = BeautifulSoup(html, 'lxml')
    base_url = 'https://www.thewhiskyexchange.com/'
    products = soup.find_all('li', class_='product-grid__item')
    products_links = []
    for product in products:
        products_links.append(base_url + product.find('a')['href'])
    return products_links


def parse_product_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_data = {
        'title': soup.find('h1', class_='product-main__name').text.strip() if soup.find('h1', class_='product-main__name') else 'not accecible',
        'price': soup.find('p', class_='product-action__price').text.strip() if soup.find('p', class_='product-action__price') else 'not accecible',
        'rating': soup.find('span',
                            class_='review-overview__rating star-rating star-rating--50').text.strip() if soup.find(
            'span', class_='review-overview__rating star-rating star-rating--50') else 'not accecible',
        'reviews_number': soup.find('span', class_='review-overview__count').text.strip().replace("\xa0", " ")[
                          1:-1] if soup.find('span', class_='review-overview__count') else 'not accecible'
    }
    return product_data


def main():
    product_links = []
    products_data = []
    for i in range(1, 3):
        url = f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={i}'
        product_links.extend(retrieve_links(code_source(url)))

    for link in product_links:
        products_data.append(parse_product_data(code_source(link)))
        print(link, 'is scraped')

    print(len(products_data))
    for i, j in zip(product_links, products_data):
        print(i, j)


if __name__ == '__main__':
    main()