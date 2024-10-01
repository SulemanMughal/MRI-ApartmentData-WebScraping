import csv
import traceback
import re
import requests
from bs4 import BeautifulSoup
import time
import logging
import vars

from datetime import datetime

# Set up logging configuration
# logging.basicConfig(filename='error_log.txt', level=logging.ERROR)

import pandas as pd


# file_name = 'urls.txt'



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


csv_output_file_path = get_timestamped_filename('apartment_data')

# Read the CSV file (replace 'urls.csv' with the correct file path)
csv_file_path = './apartment_links.csv'  # Replace with actual path
df = pd.read_csv(csv_file_path)




def get_details(apartmentId, csv_output_file_path):
    params = {
        'MODE': str(apartmentId),
        'MODE2': 'StartFromTop_Directory',
        'VIP': '010',
    }

    response = requests.get(
        'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp',
        params=params,
        cookies=vars.cookies,
        headers=vars.headers
    )

    soup = BeautifulSoup(response.content, 'html.parser')
    try:


        # Find the first <font> tag that contains "ID:", safely checking for None
        font_with_id = soup.find('font', string=lambda text: text and 'ID:' in text)
        apartment_id=None
        # Get the next sibling of the found element and extract its text
        if font_with_id and font_with_id.next_sibling:
            apartment_id = font_with_id.next_sibling.strip()  # Strip to remove extra whitespace
            # print("Apartment ID:", apartment_id)
        # else:
        #     print("Apartment ID not found.")



        # Find the first <font> tag inside the specified <div>
        apartment_title = soup.select_one('div.AptFont2Margin font font:first-child')

        # Extract and trim the text
        if apartment_title:
            apartments_title = apartment_title.get_text(strip=True)  # Using get_text() with strip=True to trim whitespace
            # print("Apartment Title:", apartments_title)
        # else:
        #     print("Apartment Title not found.")



        # Find the first <br> tag inside the specified <div>
        apartment_address_elem = soup.select_one('div.AptFont2Margin font br:first-child')


        # print(apartment_address_elem)
        # 
        if apartment_address_elem is None:
            apartment_address_elem = soup.select_one('div.AptFont2Margin font br')
        # Get the text value from the next sibling of the found <br> element
        if apartment_address_elem and apartment_address_elem.next_sibling:
            apartment_address_value = apartment_address_elem.next_sibling.strip()  # Strip to remove extra whitespace
            # print("apartmentAddress_value:", apartment_address_value)

            # Split the address by commas first to separate street, city, and state/zip
            address_parts = apartment_address_value.split(',') if apartment_address_value else []

            # Trim the whitespace from each part
            street = address_parts[0].strip() if len(address_parts) > 0 else ""
            city = address_parts[1].strip() if len(address_parts) > 1 else ""

            # Split the state and zip code (separated by space)
            state_and_zip = address_parts[2].strip().split(' ') if len(address_parts) > 2 else []

            # print("Street:", street)
            # print("City:", city)
            # print("State and Zip:", state_and_zip, state_and_zip[0])
        # else:
        #     print("Apartment address not found.")




        # Find the font element that contains "#Flrs:"
        total_number_of_floors_font = soup.select_one('div.AptFontMargin font:-soup-contains("#Flrs:") font:nth-of-type(3)')

        # Get the next sibling of the found element and extract its text
        if total_number_of_floors_font and total_number_of_floors_font.next_sibling:
            total_number_of_floors = total_number_of_floors_font.next_sibling.strip()  # Strip to remove extra whitespace
            # print("Total Number of floors:", total_number_of_floors)
        # else:
        #     print("Total Number of floors not found.")



        # Find the font element that contains "Units:"
        total_number_of_units_font = soup.select_one('div.AptFontMargin font:-soup-contains("Units:") font:nth-of-type(2)')

        # Get the next sibling of the found element and extract its text
        if total_number_of_units_font and total_number_of_units_font.next_sibling:
            total_number_of_units = total_number_of_units_font.next_sibling.strip()  # Strip to remove extra whitespace
            # print("Total Number of units:", total_number_of_units)
        # else:
        #     print("Total Number of units not found.")




        # Extracting the map number
        map_number_font = soup.select_one('div.AptFontMargin font:-soup-contains("Map#:") font:nth-of-type(4)')

        if map_number_font and map_number_font.next_sibling:
            map_number = map_number_font.next_sibling.strip()  # Strip to remove extra whitespace
            # print("Map Number:", map_number)
        # else:
        #     print("Map Number not found.")


        # Extracting the CR number
        cr_number_font = soup.select_one('div.AptFontMargin font:-soup-contains("CR:") font:nth-of-type(5) font')

        if cr_number_font and cr_number_font.next_sibling:
            cr_number = cr_number_font.next_sibling.strip()  # Strip to remove extra whitespace
            # print("CR Number:", cr_number)
        # else:
        #     print("CR Number not found.")



        # Initialize lists
        bedroom_plans = []
        floor_prices = []
        floor_sizes = []
        seen_bedrooms = set()
        plans_bedroom = []
        plans_bathroom = []

        # Select the relevant elements
        # floor_plans_elements = soup.select("a[name='EBROCHURE_FLOORPLANS'] div.AptFont2 b table.Apt2 tbody tr td b:-soup-contains('Bedroom')")
        floor_plans_elements = soup.select("a[name='EBROCHURE_FLOORPLANS'] div.AptFont2 b table.Apt2 b:-soup-contains('Bedroom')")

        # print(floor_plans_elements)

        for index, element in enumerate(floor_plans_elements):
            text = element.get_text(strip=True)

            # Match text like "1 Bedroom", "2 Bedrooms", etc.
            if re.match(r'\d+ Bedroom', text):
                # If the bedroom type has not been seen, add it to the set and allow it
                if text not in seen_bedrooms:
                    seen_bedrooms.add(text)
                    bedroom_plans.append(f"{text} Plan")  # Add "Plan" to the bedroom type

                    # Get parent elements and find required details
                    required_elements = element.find_parent('tr')
                    if required_elements:
                        # Assuming the structure is the same as in JavaScript
                        cr_number = required_elements.find_next_sibling().find_all('td')[1].get_text(strip=True)
                        floor_prices.append(cr_number)
                        
                        cr_number_2 = required_elements.find_next_sibling().find_all('td')[2].get_text(strip=True)
                        floor_sizes.append(cr_number_2)

                        plans_bedroom.append(index + 1)
                        plans_bathroom.append(index + 1)

        # Joining lists for output
        bedroom_plan_string = '|'.join(bedroom_plans)
        bedroom_price_string = '|'.join(floor_prices)
        bedroom_size_string = '|'.join(floor_sizes)
        plans_bedroom_string = '|'.join(map(str, plans_bedroom))
        plans_bathroom_string = '|'.join(map(str, plans_bathroom))

        # Print results
        # print(bedroom_plan_string, bedroom_price_string, bedroom_size_string, plans_bedroom_string, plans_bathroom_string)



        # Extract the content of the script that contains `ShowMap_EBrochure`
        script_content = ''
        for script in soup.find_all('script'):
            if 'ShowMap_EBrochure' in script.string:
                script_content = script.string
                break  # Exit after finding the first matching script

        # Now, if the script_content has been found, proceed to extract parameters
        if script_content:
            # Extract the string inside the single quotes
            url_match = re.search(r"'([^']+)'", script_content)
            if url_match:
                url = url_match.group(1)  # Get the matched URL string

                # Get the part after '?'
                query_string = url.split('?')[1] if '?' in url else ''
                
                # Parse the query string into a dictionary
                params = dict(re.findall(r'(\w+)=([^&]+)', query_string))

                # Extract the required parameters
                mode = params.get('MODE')
                map_width = params.get('MAP_WIDTH')
                map_height = params.get('MAP_HEIGHT')
                map_center_lat = params.get('MAP_CENTER_LAT')
                map_center_lng = params.get('MAP_CENTER_LNG')
                map_point_lat = params.get('MAP_POINT_LAT')
                map_point_lng = params.get('MAP_POINT_LNG')
                map_zoom_level = params.get('MAP_ZOOMLEVEL')
                map_use_point_info = params.get('MAP_USEPOINTINFO')
                map_use_map_click = params.get('MAP_USEMAPCLICK_LAT_LNG')
                map_use_address = params.get('MAP_USEADDRESS')

                with open(csv_output_file_path,  mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    
                    data = [
                        apartment_id,
                        apartments_title,
                        state_and_zip[0],
                        city,
                        bedroom_price_string.split("|")[0].split("-")[0].replace('$', '').replace(',', '') ,
                        bedroom_price_string.split("|")[-1].split("-")[-1].replace('$', '').replace(',', '') ,
                        bedroom_size_string.split("|")[0].split("-")[0].replace('$', '').replace(',', ''),  # 
                        bedroom_size_string.split("|")[-1].split("-")[-1].replace('$', '').replace(',', ''),
                        plans_bedroom_string.split("|")[0],
                        plans_bedroom_string.split("|")[-1],
                        plans_bathroom_string.split("|")[0],
                        plans_bathroom_string.split("|")[-1],
                        apartment_address_value,
                        state_and_zip[-1],
                        bedroom_plan_string,
                        '|'.join([price.split('-')[0].replace('$', '').replace(',', '') for price in bedroom_price_string.split("|")]),
                        '|'.join([size.split("-")[0].replace(",", "") for size in bedroom_size_string.split("|")]),
                        plans_bedroom_string,
                        plans_bathroom_string,
                        apartment_address_value,
                        f"{map_point_lat},{map_point_lng}"
                    ]
                    writer.writerow(data)
            # else:
            #     print("URL not found in script content.")
        # else:
        #     print("Script content with ShowMap_EBrochure not found.")

    except:
        # traceback.print_exc()
        # logging.error(f"Exception occurred for apartment ID: {apartmentId}", exc_info=True)

        logging.error("Exception occurred", exc_info=True)