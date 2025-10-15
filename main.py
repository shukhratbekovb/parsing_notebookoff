import requests
from bs4 import BeautifulSoup

URL = "https://notebookoff.uz/catalog/"
HOST = "https://notebookoff.uz"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
}


def get_soup(link):
    response = requests.get(link, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_categories():
    soup = get_soup(URL)
    categories = soup.find_all("a", class_="bigTitle")
    data = []
    for category in categories:
        title = category.text
        link = HOST + category.get("href")
        data.append(
            {
                "title": title,
                "link": link,
            }
        )
    return data

def get_characteristics(link):
    pass
    # { "key":""}
def get_products(link):
    soup = get_soup(link)
    products = soup.find_all("div", class_="item product sku")
    data = []
    for product in products:
        title = product.find("a", class_="name").text.strip()
        link = HOST + product.find("a", class_="name").get("href")
        price = product.find("a", class_="price").text.strip().replace("/ Без НДС", "").strip()
        img = HOST + product.find("a", class_="picture").find("img").get("src")
        markers = [
            marker.text.strip()
            for marker in product.find_all("div", class_="marker")
        ]
        data.append({
            "title": title,
            "link": link,
            "price": price.replace("\xa0", ""),
            "img": img,
            "markers": markers,
            "characteristics": get_characteristics(link)
        })
    return data



def main():
    data = get_categories()
    for category in data:
        category["products"] = get_products(category["link"])
    print(data)

if __name__ == "__main__":
    main()