import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL (practice site)
BASE_URL = "http://quotes.toscrape.com/page/{}/"

def get_soup(url):
    """Fetch page and return BeautifulSoup object."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_jobs_from_page(soup):
    """Extract data from a single page and return as list of dictionaries."""
    jobs_data = []
    quotes = soup.find_all("div", class_="quote")  # Using quotes as "jobs"

    for q in quotes:
        title = q.find("span", class_="text").text
        company = q.find("small", class_="author").text
        location = "Remote"  # placeholder
        salary = "N/A"       # placeholder

        jobs_data.append({
            "Job Title": title,
            "Company": company,
            "Location": location,
            "Salary": salary
        })
    return jobs_data

def main():
    all_jobs = []
    pages_to_scrape = 5  # scrape first 5 pages

    for page in range(1, pages_to_scrape + 1):
        url = BASE_URL.format(page)
        print(f"Scraping page {page}...")
        soup = get_soup(url)
        if soup:
            jobs = extract_jobs_from_page(soup)
            if jobs:
                all_jobs.extend(jobs)
            else:
                print(f"No data found on page {page}")
        else:
            print(f"Skipping page {page} due to error")

    if not all_jobs:
        print("No data scraped. Exiting.")
        return

    # Create dataframe
    df = pd.DataFrame(all_jobs)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Optional keyword filter
    keyword = input("Enter keyword to filter jobs (leave blank to skip): ").strip()
    if keyword:
        df = df[df['Job Title'].str.contains(keyword, case=False, na=False)]

    # Export to CSV
    df.to_csv("jobs_output.csv", index=False)
    print(f"Data exported successfully! Total rows: {len(df)}")

if __name__ == "__main__":
    main()