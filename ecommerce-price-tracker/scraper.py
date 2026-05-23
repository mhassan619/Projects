import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"


def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_books_from_page(soup):
    books_data = []
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        name = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]

        price_number = float(price.replace("£", "").replace("Â", "").strip())
        
        # Price category logic
        if price_number < 20:
            category = "Cheap"
        elif price_number < 40:
            category = "Medium"
        else:
            category = "Expensive"

        books_data.append({
            "Product Name": name,
            "Price (£)": price_number,
            "Rating": rating,
            "Category": category,
            "Scraped At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return books_data


def main():
    all_books = []

    # Scrape first 5 pages
    for page in range(1, 6):
        url = BASE_URL.format(page)
        print(f"Scraping page {page}...")
        soup = get_soup(url)

        if soup:
            books = extract_books_from_page(soup)
            all_books.extend(books)

    if all_books:
        df = pd.DataFrame(all_books)
        df.sort_values(by="Price (£)", inplace=True)
        df.to_excel("output.xlsx", index=False)
        print("Data exported successfully to output.xlsx")
    else:
        print("No data scraped.")


if __name__ == "__main__":
    main()