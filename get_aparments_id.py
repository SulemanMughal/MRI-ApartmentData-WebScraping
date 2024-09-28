import re
import requests
from bs4 import BeautifulSoup
import time

from datetime import datetime
import get_apartment_details
import csv

headers = [
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
    return f"{base_name}_{timestamp}.csv"


output_file_path = get_timestamped_filename('apartment_data')

with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    # writer = csv.writer(file)
    # writer.writerow(headers)
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()  # Write headers

# URL to scrape
url = 'https://www.apartmentdata.com/EXERequest/ADC_ShowResults.asp'
cookies = {
    '_gid': 'GA1.2.1913137885.1727479579',
    '__utmc': '50201974',
    '__utmz': '50201974.1727521770.12.7.utmccn=(referral)|utmcsr=us.apartmentdata.com|utmcct=/|utmcmd=referral',
    'ASPSESSIONIDCUATACSB': 'AMFIOCODNBAHAKAPNGJGIDGE',
    '__utma': '50201974.1315800874.1726249570.1727538170.1727542760.15',
    '__utmb': '50201974',
    '_ga': 'GA1.1.1315800874.1726249570',
    '_ga_WGPY1JWDFK': 'GS1.1.1727542774.16.0.1727542780.0.0.0',
    'ADS': 'G1=%7EADC%5FZ%5F100028%7Eadc%5Fz%5F1000%7EADC%5FZ%5F100120240928115944%7Eadc%5Fz%5F1001%7EADC%5FZ%5F10020%7Eadc%5Fz%5F1002%7EADC%5FZ%5F10070%7Eadc%5Fz%5F1007%7EADC%5FZ%5F10081%7Eadc%5Fz%5F1008%7EADC%5FZ%5F1009F%7Eadc%5Fz%5F1009%7EADC%5FZ%5F1010Y%7Eadc%5Fz%5F1010%7EADC%5FZ%5F1011N%7Eadc%5Fz%5F1011%7EADC%5FZ%5F101310061%7Eadc%5Fz%5F1013%7EADC%5FZ%5F10154291A%7Eadc%5Fz%5F1015%7EADC%5FZ%5F1016TX%7Eadc%5Fz%5F1016%7EADC%5FZ%5F1017TXHO%7Eadc%5Fz%5F1017%7EADC%5FZ%5F1018TXHO%7Eadc%5Fz%5F1018%7EADC%5FZ%5F10190%7Eadc%5Fz%5F1019%7EADC%5FZ%5F102099999%7Eadc%5Fz%5F1020%7EADC%5FZ%5F1021X%7Eadc%5Fz%5F1021%7EADC%5FZ%5F1022X%7Eadc%5Fz%5F1022%7EADC%5FZ%5F102310%7Eadc%5Fz%5F1023%7EADC%5FZ%5F1024HSVI%7Eadc%5Fz%5F1024%7EADC%5FZ%5F10251900%7Eadc%5Fz%5F1025%7EADC%5FZ%5F10269999%7Eadc%5Fz%5F1026%7EADC%5FZ%5F10271%7Eadc%5Fz%5F1027%7EADC%5FZ%5F10289999%7Eadc%5Fz%5F1028%7EADC%5FZ%5F10291%7Eadc%5Fz%5F1029%7EADC%5FZ%5F10309999%7Eadc%5Fz%5F1030%7EADC%5FZ%5F1034Y%7Eadc%5Fz%5F1034%7EADC%5FZ%5F10351%7Eadc%5Fz%5F1035%7EADC%5FZ%5F10360%7Eadc%5Fz%5F1036%7EADC%5FZ%5F10370%7Eadc%5Fz%5F1037%7EADC%5FZ%5F10380%2E00%7Eadc%5Fz%5F1038%7EADC%5FZ%5F1050AR%7Eadc%5Fz%5F1050%7EADC%5FZ%5F105150%7Eadc%5Fz%5F1051%7EADC%5FZ%5F1053A%7Eadc%5Fz%5F1053%7EADC%5FZ%5F10571%7Eadc%5Fz%5F1057%7EADC%5FZ%5F11000%7Eadc%5Fz%5F1100%7EADC%5FZ%5F11020%7Eadc%5Fz%5F1102%7EADC%5FZ%5F11030%7Eadc%5Fz%5F1103%7EADC%5FZ%5F11045%7Eadc%5Fz%5F1104%7EADC%5FZ%5F11060%7Eadc%5Fz%5F1106%7EADC%5FZ%5F11070%7Eadc%5Fz%5F1107%7EADC%5FZ%5F11085%7Eadc%5Fz%5F1108%7EADC%5FZ%5F1109P%7Eadc%5Fz%5F1109%7EADC%5FZ%5F11220%7Eadc%5Fz%5F1122%7EADC%5FZ%5F11230%7Eadc%5Fz%5F1123%7EADC%5FZ%5F11245%7Eadc%5Fz%5F1124%7EADC%5FZ%5F11255%7Eadc%5Fz%5F1125%7EADC%5FZ%5F11265%7Eadc%5Fz%5F1126%7EADC%5FZ%5F11275%7Eadc%5Fz%5F1127%7EADC%5FZ%5F11280%7Eadc%5Fz%5F1128%7EADC%5FZ%5F11290%7Eadc%5Fz%5F1129%7EADC%5FZ%5F120063939%7Eadc%5Fz%5F1200%7EADC%5FZ%5F12013863%7Eadc%5Fz%5F1201%7EADC%5FZ%5F1202Y%7Eadc%5Fz%5F1202%7EADC%5FZ%5F1205Y%7Eadc%5Fz%5F1205%7EADC%5FZ%5F1207ReLoad%7Eadc%5Fz%5F1207%7EADC%5FZ%5F1220147%7Eadc%5Fz%5F1220%7EADC%5FZ%5F122120240928115940%7Eadc%5Fz%5F1221%7EADC%5FZ%5F1230151%7Eadc%5Fz%5F1230%7EADC%5FZ%5F123120240928115939%7Eadc%5Fz%5F1231%7EADC%5FZ%5F1232Y%7Eadc%5Fz%5F1232%7EADC%5FZ%5F1233TXHO%7Eadc%5Fz%5F1233%7EADC%5FZ%5F1236Y%3A%7Eadc%5Fz%5F1236%7EADC%5FZ%5F1237N%7Eadc%5Fz%5F1237%7EADC%5FZ%5F123809%2F26%2F2024%7Eadc%5Fz%5F1238%7EADC%5FZ%5F1251Apartment+Wolf%7Eadc%5Fz%5F1251%7EADC%5FZ%5F125211906+Marrs+Dr%7Eadc%5Fz%5F1252%7EADC%5FZ%5F1254Houston%7Eadc%5Fz%5F1254%7EADC%5FZ%5F1255TX%7Eadc%5Fz%5F1255%7EADC%5FZ%5F125677065%7Eadc%5Fz%5F1256%7EADC%5FZ%5F1257281%2F701%2D0336%7Eadc%5Fz%5F1257%7EADC%5FZ%5F1260210%2F540%2D1552%7Eadc%5Fz%5F1260%7EADC%5FZ%5F1262http%3A%2F%2Fwww%2EApartmentWolf%2Ecom%7Eadc%5Fz%5F1262%7EADC%5FZ%5F1268%5EI1830%5Ei18%5EI19Basic%5Ei19%7Eadc%5Fz%5F1268%7EADC%5FZ%5F130063939%7Eadc%5Fz%5F1300%7EADC%5FZ%5F1301Alex%7Eadc%5Fz%5F1301%7EADC%5FZ%5F1302Taylor%7Eadc%5Fz%5F1302%7EADC%5FZ%5F1303281%2F701%2D0336%7Eadc%5Fz%5F1303%7EADC%5FZ%5F1306alex%40apartmentwolf%2Ecom%7Eadc%5Fz%5F1306%7EADC%5FZ%5F1307TX%5F613630%7Eadc%5Fz%5F1307%7EADC%5FZ%5F1400ADC%5FDefault%2Egif%7Eadc%5Fz%5F1400%7EADC%5FZ%5F1403%23000000%7Eadc%5Fz%5F1403%7EADC%5FZ%5F1404%23FFFFFF%7Eadc%5Fz%5F1404%7EADC%5FZ%5F1406%23000000%7Eadc%5Fz%5F1406%7EADC%5FZ%5F1407%2381C8F2%7Eadc%5Fz%5F1407%7EADC%5FZ%5F1409%23000000%7Eadc%5Fz%5F1409%7EADC%5FZ%5F1410%23DEEBF7%7Eadc%5Fz%5F1410%7EADC%5FZ%5F1413GrayBlack%2F%7Eadc%5Fz%5F1413%7EADC%5FZ%5F1500A%7Eadc%5Fz%5F1500%7EADC%5FZ%5F1502N%7Eadc%5Fz%5F1502%7EADC%5FZ%5F1503TX%2F%7Eadc%5Fz%5F1503%7EADC%5FZ%5F1772TX%7Eadc%5Fz%5F1772%7EADC%5FZ%5F1773TXHO%7Eadc%5Fz%5F1773&G4=20240928115937&G3=10061&A1=T&G2=alex%40apartmentwolf%2Ecom&B1=75%2D812239%2D343463',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': '_gid=GA1.2.1913137885.1727479579; __utmc=50201974; __utmz=50201974.1727521770.12.7.utmccn=(referral)|utmcsr=us.apartmentdata.com|utmcct=/|utmcmd=referral; ASPSESSIONIDCUATACSB=AMFIOCODNBAHAKAPNGJGIDGE; __utma=50201974.1315800874.1726249570.1727538170.1727542760.15; __utmb=50201974; _ga=GA1.1.1315800874.1726249570; _ga_WGPY1JWDFK=GS1.1.1727542774.16.0.1727542780.0.0.0; ADS=G1=%7EADC%5FZ%5F100028%7Eadc%5Fz%5F1000%7EADC%5FZ%5F100120240928115944%7Eadc%5Fz%5F1001%7EADC%5FZ%5F10020%7Eadc%5Fz%5F1002%7EADC%5FZ%5F10070%7Eadc%5Fz%5F1007%7EADC%5FZ%5F10081%7Eadc%5Fz%5F1008%7EADC%5FZ%5F1009F%7Eadc%5Fz%5F1009%7EADC%5FZ%5F1010Y%7Eadc%5Fz%5F1010%7EADC%5FZ%5F1011N%7Eadc%5Fz%5F1011%7EADC%5FZ%5F101310061%7Eadc%5Fz%5F1013%7EADC%5FZ%5F10154291A%7Eadc%5Fz%5F1015%7EADC%5FZ%5F1016TX%7Eadc%5Fz%5F1016%7EADC%5FZ%5F1017TXHO%7Eadc%5Fz%5F1017%7EADC%5FZ%5F1018TXHO%7Eadc%5Fz%5F1018%7EADC%5FZ%5F10190%7Eadc%5Fz%5F1019%7EADC%5FZ%5F102099999%7Eadc%5Fz%5F1020%7EADC%5FZ%5F1021X%7Eadc%5Fz%5F1021%7EADC%5FZ%5F1022X%7Eadc%5Fz%5F1022%7EADC%5FZ%5F102310%7Eadc%5Fz%5F1023%7EADC%5FZ%5F1024HSVI%7Eadc%5Fz%5F1024%7EADC%5FZ%5F10251900%7Eadc%5Fz%5F1025%7EADC%5FZ%5F10269999%7Eadc%5Fz%5F1026%7EADC%5FZ%5F10271%7Eadc%5Fz%5F1027%7EADC%5FZ%5F10289999%7Eadc%5Fz%5F1028%7EADC%5FZ%5F10291%7Eadc%5Fz%5F1029%7EADC%5FZ%5F10309999%7Eadc%5Fz%5F1030%7EADC%5FZ%5F1034Y%7Eadc%5Fz%5F1034%7EADC%5FZ%5F10351%7Eadc%5Fz%5F1035%7EADC%5FZ%5F10360%7Eadc%5Fz%5F1036%7EADC%5FZ%5F10370%7Eadc%5Fz%5F1037%7EADC%5FZ%5F10380%2E00%7Eadc%5Fz%5F1038%7EADC%5FZ%5F1050AR%7Eadc%5Fz%5F1050%7EADC%5FZ%5F105150%7Eadc%5Fz%5F1051%7EADC%5FZ%5F1053A%7Eadc%5Fz%5F1053%7EADC%5FZ%5F10571%7Eadc%5Fz%5F1057%7EADC%5FZ%5F11000%7Eadc%5Fz%5F1100%7EADC%5FZ%5F11020%7Eadc%5Fz%5F1102%7EADC%5FZ%5F11030%7Eadc%5Fz%5F1103%7EADC%5FZ%5F11045%7Eadc%5Fz%5F1104%7EADC%5FZ%5F11060%7Eadc%5Fz%5F1106%7EADC%5FZ%5F11070%7Eadc%5Fz%5F1107%7EADC%5FZ%5F11085%7Eadc%5Fz%5F1108%7EADC%5FZ%5F1109P%7Eadc%5Fz%5F1109%7EADC%5FZ%5F11220%7Eadc%5Fz%5F1122%7EADC%5FZ%5F11230%7Eadc%5Fz%5F1123%7EADC%5FZ%5F11245%7Eadc%5Fz%5F1124%7EADC%5FZ%5F11255%7Eadc%5Fz%5F1125%7EADC%5FZ%5F11265%7Eadc%5Fz%5F1126%7EADC%5FZ%5F11275%7Eadc%5Fz%5F1127%7EADC%5FZ%5F11280%7Eadc%5Fz%5F1128%7EADC%5FZ%5F11290%7Eadc%5Fz%5F1129%7EADC%5FZ%5F120063939%7Eadc%5Fz%5F1200%7EADC%5FZ%5F12013863%7Eadc%5Fz%5F1201%7EADC%5FZ%5F1202Y%7Eadc%5Fz%5F1202%7EADC%5FZ%5F1205Y%7Eadc%5Fz%5F1205%7EADC%5FZ%5F1207ReLoad%7Eadc%5Fz%5F1207%7EADC%5FZ%5F1220147%7Eadc%5Fz%5F1220%7EADC%5FZ%5F122120240928115940%7Eadc%5Fz%5F1221%7EADC%5FZ%5F1230151%7Eadc%5Fz%5F1230%7EADC%5FZ%5F123120240928115939%7Eadc%5Fz%5F1231%7EADC%5FZ%5F1232Y%7Eadc%5Fz%5F1232%7EADC%5FZ%5F1233TXHO%7Eadc%5Fz%5F1233%7EADC%5FZ%5F1236Y%3A%7Eadc%5Fz%5F1236%7EADC%5FZ%5F1237N%7Eadc%5Fz%5F1237%7EADC%5FZ%5F123809%2F26%2F2024%7Eadc%5Fz%5F1238%7EADC%5FZ%5F1251Apartment+Wolf%7Eadc%5Fz%5F1251%7EADC%5FZ%5F125211906+Marrs+Dr%7Eadc%5Fz%5F1252%7EADC%5FZ%5F1254Houston%7Eadc%5Fz%5F1254%7EADC%5FZ%5F1255TX%7Eadc%5Fz%5F1255%7EADC%5FZ%5F125677065%7Eadc%5Fz%5F1256%7EADC%5FZ%5F1257281%2F701%2D0336%7Eadc%5Fz%5F1257%7EADC%5FZ%5F1260210%2F540%2D1552%7Eadc%5Fz%5F1260%7EADC%5FZ%5F1262http%3A%2F%2Fwww%2EApartmentWolf%2Ecom%7Eadc%5Fz%5F1262%7EADC%5FZ%5F1268%5EI1830%5Ei18%5EI19Basic%5Ei19%7Eadc%5Fz%5F1268%7EADC%5FZ%5F130063939%7Eadc%5Fz%5F1300%7EADC%5FZ%5F1301Alex%7Eadc%5Fz%5F1301%7EADC%5FZ%5F1302Taylor%7Eadc%5Fz%5F1302%7EADC%5FZ%5F1303281%2F701%2D0336%7Eadc%5Fz%5F1303%7EADC%5FZ%5F1306alex%40apartmentwolf%2Ecom%7Eadc%5Fz%5F1306%7EADC%5FZ%5F1307TX%5F613630%7Eadc%5Fz%5F1307%7EADC%5FZ%5F1400ADC%5FDefault%2Egif%7Eadc%5Fz%5F1400%7EADC%5FZ%5F1403%23000000%7Eadc%5Fz%5F1403%7EADC%5FZ%5F1404%23FFFFFF%7Eadc%5Fz%5F1404%7EADC%5FZ%5F1406%23000000%7Eadc%5Fz%5F1406%7EADC%5FZ%5F1407%2381C8F2%7Eadc%5Fz%5F1407%7EADC%5FZ%5F1409%23000000%7Eadc%5Fz%5F1409%7EADC%5FZ%5F1410%23DEEBF7%7Eadc%5Fz%5F1410%7EADC%5FZ%5F1413GrayBlack%2F%7Eadc%5Fz%5F1413%7EADC%5FZ%5F1500A%7Eadc%5Fz%5F1500%7EADC%5FZ%5F1502N%7Eadc%5Fz%5F1502%7EADC%5FZ%5F1503TX%2F%7Eadc%5Fz%5F1503%7EADC%5FZ%5F1772TX%7Eadc%5Fz%5F1772%7EADC%5FZ%5F1773TXHO%7Eadc%5Fz%5F1773&G4=20240928115937&G3=10061&A1=T&G2=alex%40apartmentwolf%2Ecom&B1=75%2D812239%2D343463',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

params = {
    'SHOWPAGE': '1',
    'VIP': '000',
}




# Fetch the page content
response = requests.get(url,
                         params=params,
    cookies=cookies,
    headers=headers)
response.raise_for_status()  # Check for successful request


# print(response)

# print(response.content)

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
        get_apartment_details.get_details(href.split(":")[-1].strip(), output_file_path, headers)



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
    time.sleep(2)
    print("----------------")
    print("current page : ",  i)
    params = {
        'SHOWPAGE': str(i),
        'VIP': '000',
    }

    
    # Fetch the page content
    response = requests.get(url,
                            params=params,
        cookies=cookies,
        headers=headers)
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
            get_apartment_details.get_details(href.split(":")[-1].strip(), output_file_path, headers)

