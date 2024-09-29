import pandas as pd


import open_browser
import csv

from datetime import datetime

import get_apartment_details
import get_apartment_list


# Convert Selenium cookies to a dictionary that requests can use
def selenium_cookies_to_requests(cookies):
    cookie_dict = {}
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
    return cookie_dict

TARGET_URL="https://www.apartmentdata.com/EXERequest/ADC_ShowResults.asp"

csv_headers = [
    "real_estate_property_identity",
    "Title",
    "Province / State",
    "City / Town",
    "real_estate_property_price_short",
    "real_estate_second-price",
    "real_estate_property_size",
    "real_estate_second-size",
    "real_estate_property_bedrooms",
    "real_estate_second-bedroom",
    "real_estate_property_bathrooms",
    "real_estate_second-bathroom",
    "real_estate_property_address",
    "real_estate_property_zip",
    "Floor Plans_floor_name",
    "Floor Plans_floor_price",
    "Floor Plans_floor_size",
    "Floor Plans_bedroom",
    "Floor Plans_bathroom",
    "Extra Address Field",
    "Extra Latitude Field"
]


def get_timestamped_filename(base_name, fmt="%Y-%m-%d_%H-%M-%S"):
    """Generate a timestamped filename."""
    timestamp = datetime.now().strftime(fmt)
    print(f"{base_name}_{timestamp}.csv")
    return f"{base_name}_{timestamp}.csv"


output_file_path = get_timestamped_filename('apartment_data')

# Read the CSV file (replace 'urls.csv' with the correct file path)
csv_file_path = './urls.csv'  # Replace with actual path
df = pd.read_csv(csv_file_path)







with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()  





# Iterate through the URLs one by one
for index, row in df.iterrows():
    url = row['URL']
    print(f"Processing URL {index + 1}: {url}")

    
    # Here, you can perform actions on the URL like opening it with Selenium, etc.
    # For example:
    # driver.get(url)

    (cookies, params, headers) = open_browser.get_response(url)
    # print((cookies, params, headers))
    cookies = selenium_cookies_to_requests(cookies)
    # print(cookies)
    get_apartment_list.get_aparment_list(
        TARGET_URL,
        params, 
        cookies, 
        headers,
        output_file_path
    )
