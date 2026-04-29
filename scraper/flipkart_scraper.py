import pandas as pd
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape(search_query, num_pages=5):
    driver = get_driver()
    products = []

    for page in range(1, num_pages+1):
        url = f"https://www.flipkart.com/search?q={search_query}&page={page}"

        try:
            driver.get(url)
            time.sleep(random.uniform(2, 4))

            cards = driver.find_elements(By.CSS_SELECTOR, "div[data-id]")

            for card in cards:
                try:
                    name = card.find_element(By.CLASS_NAME, "RG5Slk").text.strip()
                except: name = None
                try:
                    price = card.find_element(By.CLASS_NAME, "hZ3P6w").text.strip()
                except: price = None
                try:
                    rating = card.find_element(By.CLASS_NAME, "MKiFS6").text.strip()
                except: rating = None
                try:
                    image = card.find_element(By.CLASS_NAME, "UCc1lI").get_attribute("src")
                except: image = None

                products.append({
                    "name": name,
                    "price": price,
                    "rating": rating,
                    "image": image
                })

            print(f"Page {page} done — {len(cards)} products found")
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"Page {page} error: {e}")
            continue

    driver.quit()
    df = pd.DataFrame(products)
    df.drop_duplicates(subset=["name", "price"], inplace=True)
    print(f"After dedup: {len(df)} unique products")
    df.to_csv("data/flipkart_data.csv", index=False)
    print(f"Total: {len(df)} products saved!")
    return df

if __name__ == "__main__":
    df = scrape("smartphones", num_pages=5)
    print(df.head())