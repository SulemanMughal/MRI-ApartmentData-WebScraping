from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import csv
import os
from datetime import datetime

# Set up Selenium with Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize the WebDriver (replace with your ChromeDriver path if needed)
driver = webdriver.Chrome(options=options)

# Define a function to scrape a website with cookies
def scrape_website_with_cookies(driver, target_url):
    try:
        # Load cookies from cookies.json
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)
        
        # Navigate to the target URL
        driver.get(target_url)
        
        # Add cookies to the session
        for cookie in cookies:
            driver.add_cookie(cookie)
        
        driver.refresh()  # Reload the page with cookies
        
        # Get page content and parse with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extract data (Modify based on your selectors)
        apartment_id = soup.select_one('div.AptFontMargin font:contains("ID:")').text.strip()
        apartment_title = soup.select_one('div.AptFont2Margin font font:first').text.strip()
        apartment_address = soup.select_one('div.AptFont2Margin font br:first').next_sibling.strip()

        # Split the address into components
        address_parts = apartment_address.split(',')
        street = address_parts[0].strip()
        city = address_parts[1].strip()
        state_and_zip = address_parts[2].strip().split(' ')
        state = state_and_zip[0].strip()
        zip_code = state_and_zip[1].strip()

        # Output scraped data
        print(f"Apartment ID: {apartment_id}")
        print(f"Apartment Title: {apartment_title}")
        print(f"Street: {street}, City: {city}, State: {state}, Zip: {zip_code}")
        
        return {
            "Apartment ID": apartment_id,
            "Title": apartment_title,
            "Street": street,
            "City": city,
            "State": state,
            "Zip": zip_code
        }
    
    except Exception as e:
        print(f"Error scraping {target_url}: {e}")
        return None

# Write data to CSV
def write_to_csv(data, filename):
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    else:
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writerows(data)

# Main function
def main():
    target_urls = ['https://example.com/page1', 'https://example.com/page2']  # Replace with your URLs

    # Generate timestamp for filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"apartment_data_{timestamp}.csv"

    all_data = []
    
    for target_url in target_urls:
        scraped_data = scrape_website_with_cookies(driver, target_url)
        if scraped_data:
            all_data.append(scraped_data)
    
    if all_data:
        write_to_csv(all_data, filename)
        print(f"Data saved to {filename}")
    
    driver.quit()

if __name__ == "__main__":
    main()
