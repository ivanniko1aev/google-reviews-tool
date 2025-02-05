from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
from datetime import datetime

# Function to scrape Google reviews
def get_google_reviews(google_maps_url, max_reviews=20):
    # Set up headless Chrome
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Automatically manage ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the Google Maps URL
    driver.get(google_maps_url)
    time.sleep(5)  # Wait for the page to load

    # Scroll to load more reviews
    scrollable_div = driver.find_element(By.XPATH, '//div[@role="main"]')
    for _ in range(5):  # Adjust this to load more reviews
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(2)

    # Get page source after content has loaded
    html_content = driver.page_source
    driver.quit()

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    reviews = []

    # Extract review elements
    review_elements = soup.find_all('div', class_='jftiEf fontBodyMedium')
    for review in review_elements[:max_reviews]:
        author = review.find('div', class_='d4r55')
        rating = review.find('span', class_='kvMYJc')
        content = review.find('span', class_='wiI7pd')

        reviews.append({
            'author': author.get_text(strip=True) if author else 'N/A',
            'rating': rating.get('aria-label') if rating else 'N/A',
            'content': content.get_text(strip=True) if content else 'N/A'
        })

    return reviews

# Save reviews to CSV
def save_reviews_to_csv(reviews):
    filename = f"google_reviews_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["author", "rating", "content"])
        writer.writeheader()
        writer.writerows(reviews)
    print(f"✅ Reviews saved to {filename}")

# Main execution
if __name__ == "__main__":
    google_maps_url = "https://maps.app.goo.gl/eDN7cRz5JqfNNYd57"  # Replace with your Google Maps link
    print("🔍 Scraping reviews...")

    reviews = get_google_reviews(google_maps_url)

    if reviews:
        for idx, review in enumerate(reviews, start=1):
            print(f"\nReview #{idx}")
            print(f"Author: {review['author']}")
            print(f"Rating: {review['rating']}")
            print(f"Content: {review['content']}")

        save_reviews_to_csv(reviews)
    else:
        print("⚠️ No reviews found.")
