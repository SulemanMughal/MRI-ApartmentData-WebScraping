import re
import requests
from bs4 import BeautifulSoup
import time

from datetime import datetime
import get_apartment_details
import csv

import vars

# URL to scrape
url = vars.TARGET_URL

output_file_path = vars.get_timestamped_filename('apartment_data')

with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=vars.csv_headers)
    writer.writeheader()  







# Fetch the page content
response = requests.get(url,
                         params=vars.params,
    cookies=vars.cookies,
    headers=vars.headers)
response.raise_for_status()  # Check for successful request



soup = BeautifulSoup(response.content, 'html.parser')
anchors = soup.select('table.Apt2 a')
for anchor in anchors:
    href = anchor.get('name')  # Get the href attribute of the anchor
    if href:
        print(f"Link: {href}")
        get_apartment_details.get_details(href.split(":")[-1].strip(), output_file_path, vars.headers)



# Find the <font> tag that contains the page number information
page_info = soup.find('font', string=re.compile(r'Page #\d+ of \d+'))

# Extract the current page and total pages using regular expressions
if page_info:
    match = re.search(r'Page #(\d+) of (\d+)', page_info.text)
    if match:
        current_page = match.group(1)
        total_pages = match.group(2)
        print(f"Current Page: {current_page}")
        print(f"Total Pages: {total_pages}")
    else:
        print("Could not find current or total pages.")
else:
    print("Could not find the page information.")



for i in range(2, int(total_pages)+1):
    time.sleep(5)
    print("----------------")
    print("current page : ",  i)
    params = {
        'SHOWPAGE': str(i),
        'VIP': '000',
    }

    
    # Fetch the page content
    response = requests.get(url,
                            params=params,
        cookies=vars.cookies,
        headers=vars.headers)
    response.raise_for_status()  # Check for successful request

    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags inside <table> tags with class "Apt2"
    # anchors = soup.select('table.Apt2 tbody tr td a')
    anchors = soup.select('table.Apt2 a')

    # Loop through the found anchors and extract the href attribute and text
    for anchor in anchors:
        href = anchor.get('name')  # Get the href attribute of the anchor
        if href:
            # text_value = anchor.text.strip()  # Get the text inside the anchor

            # Print the extracted href and associated text
            # print(f"Link: {href}, Text: {text_value}")
            print(f"Link: {href}")
            get_apartment_details.get_details(href.split(":")[-1].strip(), output_file_path, vars.headers)

