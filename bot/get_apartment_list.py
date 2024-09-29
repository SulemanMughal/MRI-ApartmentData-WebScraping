import re
import requests
from bs4 import BeautifulSoup
import time

from datetime import datetime
import get_apartment_details
import csv

# import vars

# URL to scrape
# url = vars.TARGET_URL



apartment_links_csv_file = "apartment_links.csv"


# with open(apartment_links_csv_file, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=["id"])
#     writer.writeheader()  




def get_aparment_list(region_url, params, cookies, headers, output_file_path):



    # Fetch the page content
    response = requests.get(
        region_url,
        params={
    'SHOWPAGE': '1',
    'VIP': '000',
},
        cookies=cookies,
        headers=headers)
    response.raise_for_status()  # Check for successful request



    soup = BeautifulSoup(response.content, 'html.parser')
    anchors = soup.select('table.Apt2 a')
    with open(apartment_links_csv_file,  mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for anchor in anchors:
            href = anchor.get('name')  # Get the href attribute of the anchor
            if href:
                # print(f"Link: {href}")
                writer.writerow([href.split(":")[-1].strip()])
                # get_apartment_details.get_details(href.split(":")[-1].strip(), cookies, headers, output_file_path)



    # Find the <font> tag that contains the page number information
    page_info = soup.find('font', string=re.compile(r'Page #\d+ of \d+'))
    try:
        # Extract the current page and total pages using regular expressions
        if page_info:
            match = re.search(r'Page #(\d+) of (\d+)', page_info.text)
            if match:
                # current_page = match.group(1)
                total_pages = match.group(2)
                # print(total_pages)
                if int(total_pages) > 0:
                    for i in range(2, int(total_pages)+1):
                        time.sleep(5)
                        # print("----------------")
                        # print("current page : ",  i)
                        # params = {
                        #     'SHOWPAGE': str(i),
                        #     'VIP': '000',
                        # }

                        
                        # Fetch the page content
                        response = requests.get(region_url,
                                                params={
                            'SHOWPAGE': str(i),
                            'VIP': '000',
                        },
                            cookies=cookies,
                            headers=headers)
                        response.raise_for_status()  # Check for successful request

                        
                        # Parse the HTML with BeautifulSoup
                        soup = BeautifulSoup(response.content, 'html.parser')

                        # Find all <a> tags inside <table> tags with class "Apt2"
                        # anchors = soup.select('table.Apt2 tbody tr td a')
                        anchors = soup.select('table.Apt2 a')

                        # Loop through the found anchors and extract the href attribute and text
                        with open(apartment_links_csv_file,  mode='a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            for anchor in anchors:
                                href = anchor.get('name')  # Get the href attribute of the anchor
                                if href:
                                    # print(f"Link: {href}")
                                    writer.writerow([href.split(":")[-1].strip()])
                                    # get_apartment_details.get_details(href.split(":")[-1].strip(), cookies, headers, output_file_path)

    except:
        pass