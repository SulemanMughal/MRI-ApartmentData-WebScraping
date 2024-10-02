
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import csv
import os
from urllib.parse import urljoin
import json

# Setup driver
chrome_service = Service()  # Provide the path to your chromedriver
driver = webdriver.Chrome(service=chrome_service)

# URLs to scrape
urls = [
    'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=4291A&MODE2=StartFromTop_Directory&VIP=010',
    'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp?MODE=1616A&MODE2=StartFromTop_Directory&VIP=010',
    # Add more URLs as needed
]


# Path to your cookies.json file
cookies_file_path = 'cookies.json'



# Read the cookies from the file
with open(cookies_file_path, 'r') as file:
    cookies = json.load(file)


# # Read the cookies from the file
# with open(cookies_file_path, 'r') as file:
#     cookies = json.load(file)

# Set each cookie in the browser
for cookie in cookies:
    # Add the cookie to the browser
    driver.add_cookie(cookie)

    

# # Refresh the page or navigate to another page after setting the cookies
# driver.refresh()


# File for storing the scraped data
csv_file = open('apartment_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
# csv_writer.writerow(['Property Name', 'Address', 'Type', 'Price', 'Size (sf)', 'Floor Plan', 'Description'])
csv_writer.writerow([
        'ID', 'Title', 'Province / State', 'City / Town',
        'real_estate_property_price_short', 'real_estate_second-price',
        'real_estate_property_size', 'real_estate_second-size',
        'real_estate_property_bedrooms', 'real_estate_second-bedroom',
        'real_estate_property_bathrooms', 'real_estate_second-bathroom',
        'real_estate_property_address', 'real_estate_property_zip',
        'real_estate_property_location', 'Floor Plans_floor_name',
        'Floor Plans_floor_price', 'Floor Plans_floor_size',
        'Floor Plans_bedroom', 'Floor Plans_bathroom'
    ])

# Scraping function
def scrape_apartment_data(url):
    driver.get(url)
    # Add the cookie to the browser
    # driver.add_cookie(cookie)


    # Refresh the page or navigate to another page after setting the cookies
    # driver.refresh()

    time.sleep(3)  # Adjust the sleep time if needed

    # Parse the page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract property name using XPath equivalent
    property_name = soup.find('b').get_text().strip() if soup.find('b') else 'N/A'

    # Extract address (this is an example, adjust based on your needs)
    address_tag = soup.select_one('div font')  # Adjust the selector as needed
    address = address_tag.get_text().strip() if address_tag else 'N/A'

    # Extract additional details like deposit, type, price, etc.
    table_rows = soup.find_all('tr', onmouseover=True)
    
    for row in table_rows:
        type = row.find('td').get_text().strip() if row.find('td') else 'N/A'
        price = row.find_all('td')[1].get_text().strip() if len(row.find_all('td')) > 1 else 'N/A'
        size = row.find_all('td')[2].get_text().strip() if len(row.find_all('td')) > 2 else 'N/A'
        
        # Extracting image or other details
        image_tag = soup.find('img', {'name': 'IMAGE_Floorplan'})
        image_url = urljoin('https://www.apartmentdata.com', image_tag['src']) if image_tag else 'N/A'
        
        # Write data to CSV
        csv_writer.writerow([property_name, address, type, price, size, image_url, 'Description'])  # Adjust 'Description'

# Main scraping loop
for target_url in urls:
    scrape_apartment_data(target_url)

# Close the CSV file and the browser
csv_file.close()
driver.quit()

print('Scraping completed. Data saved to apartment_data.csv')
