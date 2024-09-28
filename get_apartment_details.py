import csv

import re
import requests
from bs4 import BeautifulSoup
import time


def get_details(apartment_id, csv_filepath, headers=None):
    cookies = {
        '_gid': 'GA1.2.1913137885.1727479579',
        '__utmc': '50201974',
        '__utmz': '50201974.1727521770.12.7.utmccn=(referral)|utmcsr=us.apartmentdata.com|utmcct=/|utmcmd=referral',
        'ASPSESSIONIDCUATACSB': 'AMFIOCODNBAHAKAPNGJGIDGE',
        '__utma': '50201974.1315800874.1726249570.1727538170.1727542760.15',
        '__utmb': '50201974',
        '_gat_gtag_UA_57735016_3': '1',
        '_ga': 'GA1.1.1315800874.1726249570',
        '_ga_WGPY1JWDFK': 'GS1.1.1727542774.16.0.1727542780.0.0.0',
        'ADS': 'G1=%7EADC%5FZ%5F100028%7Eadc%5Fz%5F1000%7EADC%5FZ%5F100120240928115944%7Eadc%5Fz%5F1001%7EADC%5FZ%5F10020%7Eadc%5Fz%5F1002%7EADC%5FZ%5F10070%7Eadc%5Fz%5F1007%7EADC%5FZ%5F10081%7Eadc%5Fz%5F1008%7EADC%5FZ%5F1009F%7Eadc%5Fz%5F1009%7EADC%5FZ%5F1010Y%7Eadc%5Fz%5F1010%7EADC%5FZ%5F1011N%7Eadc%5Fz%5F1011%7EADC%5FZ%5F101310061%7Eadc%5Fz%5F1013%7EADC%5FZ%5F10154291A%7Eadc%5Fz%5F1015%7EADC%5FZ%5F1016TX%7Eadc%5Fz%5F1016%7EADC%5FZ%5F1017TXHO%7Eadc%5Fz%5F1017%7EADC%5FZ%5F1018TXHO%7Eadc%5Fz%5F1018%7EADC%5FZ%5F10190%7Eadc%5Fz%5F1019%7EADC%5FZ%5F102099999%7Eadc%5Fz%5F1020%7EADC%5FZ%5F1021X%7Eadc%5Fz%5F1021%7EADC%5FZ%5F1022X%7Eadc%5Fz%5F1022%7EADC%5FZ%5F102310%7Eadc%5Fz%5F1023%7EADC%5FZ%5F1024HSVI%7Eadc%5Fz%5F1024%7EADC%5FZ%5F10251900%7Eadc%5Fz%5F1025%7EADC%5FZ%5F10269999%7Eadc%5Fz%5F1026%7EADC%5FZ%5F10271%7Eadc%5Fz%5F1027%7EADC%5FZ%5F10289999%7Eadc%5Fz%5F1028%7EADC%5FZ%5F10291%7Eadc%5Fz%5F1029%7EADC%5FZ%5F10309999%7Eadc%5Fz%5F1030%7EADC%5FZ%5F1034Y%7Eadc%5Fz%5F1034%7EADC%5FZ%5F10351%7Eadc%5Fz%5F1035%7EADC%5FZ%5F10360%7Eadc%5Fz%5F1036%7EADC%5FZ%5F10370%7Eadc%5Fz%5F1037%7EADC%5FZ%5F10380%2E00%7Eadc%5Fz%5F1038%7EADC%5FZ%5F1050AR%7Eadc%5Fz%5F1050%7EADC%5FZ%5F105150%7Eadc%5Fz%5F1051%7EADC%5FZ%5F1053A%7Eadc%5Fz%5F1053%7EADC%5FZ%5F10571%7Eadc%5Fz%5F1057%7EADC%5FZ%5F11000%7Eadc%5Fz%5F1100%7EADC%5FZ%5F11020%7Eadc%5Fz%5F1102%7EADC%5FZ%5F11030%7Eadc%5Fz%5F1103%7EADC%5FZ%5F11045%7Eadc%5Fz%5F1104%7EADC%5FZ%5F11060%7Eadc%5Fz%5F1106%7EADC%5FZ%5F11070%7Eadc%5Fz%5F1107%7EADC%5FZ%5F11085%7Eadc%5Fz%5F1108%7EADC%5FZ%5F1109P%7Eadc%5Fz%5F1109%7EADC%5FZ%5F11220%7Eadc%5Fz%5F1122%7EADC%5FZ%5F11230%7Eadc%5Fz%5F1123%7EADC%5FZ%5F11245%7Eadc%5Fz%5F1124%7EADC%5FZ%5F11255%7Eadc%5Fz%5F1125%7EADC%5FZ%5F11265%7Eadc%5Fz%5F1126%7EADC%5FZ%5F11275%7Eadc%5Fz%5F1127%7EADC%5FZ%5F11280%7Eadc%5Fz%5F1128%7EADC%5FZ%5F11290%7Eadc%5Fz%5F1129%7EADC%5FZ%5F120063939%7Eadc%5Fz%5F1200%7EADC%5FZ%5F12013863%7Eadc%5Fz%5F1201%7EADC%5FZ%5F1202Y%7Eadc%5Fz%5F1202%7EADC%5FZ%5F1205Y%7Eadc%5Fz%5F1205%7EADC%5FZ%5F1207ReLoad%7Eadc%5Fz%5F1207%7EADC%5FZ%5F1220147%7Eadc%5Fz%5F1220%7EADC%5FZ%5F122120240928115940%7Eadc%5Fz%5F1221%7EADC%5FZ%5F1230151%7Eadc%5Fz%5F1230%7EADC%5FZ%5F123120240928115939%7Eadc%5Fz%5F1231%7EADC%5FZ%5F1232Y%7Eadc%5Fz%5F1232%7EADC%5FZ%5F1233TXHO%7Eadc%5Fz%5F1233%7EADC%5FZ%5F1236Y%3A%7Eadc%5Fz%5F1236%7EADC%5FZ%5F1237N%7Eadc%5Fz%5F1237%7EADC%5FZ%5F123809%2F26%2F2024%7Eadc%5Fz%5F1238%7EADC%5FZ%5F1251Apartment+Wolf%7Eadc%5Fz%5F1251%7EADC%5FZ%5F125211906+Marrs+Dr%7Eadc%5Fz%5F1252%7EADC%5FZ%5F1254Houston%7Eadc%5Fz%5F1254%7EADC%5FZ%5F1255TX%7Eadc%5Fz%5F1255%7EADC%5FZ%5F125677065%7Eadc%5Fz%5F1256%7EADC%5FZ%5F1257281%2F701%2D0336%7Eadc%5Fz%5F1257%7EADC%5FZ%5F1260210%2F540%2D1552%7Eadc%5Fz%5F1260%7EADC%5FZ%5F1262http%3A%2F%2Fwww%2EApartmentWolf%2Ecom%7Eadc%5Fz%5F1262%7EADC%5FZ%5F1268%5EI1830%5Ei18%5EI19Basic%5Ei19%7Eadc%5Fz%5F1268%7EADC%5FZ%5F130063939%7Eadc%5Fz%5F1300%7EADC%5FZ%5F1301Alex%7Eadc%5Fz%5F1301%7EADC%5FZ%5F1302Taylor%7Eadc%5Fz%5F1302%7EADC%5FZ%5F1303281%2F701%2D0336%7Eadc%5Fz%5F1303%7EADC%5FZ%5F1306alex%40apartmentwolf%2Ecom%7Eadc%5Fz%5F1306%7EADC%5FZ%5F1307TX%5F613630%7Eadc%5Fz%5F1307%7EADC%5FZ%5F1400ADC%5FDefault%2Egif%7Eadc%5Fz%5F1400%7EADC%5FZ%5F1403%23000000%7Eadc%5Fz%5F1403%7EADC%5FZ%5F1404%23FFFFFF%7Eadc%5Fz%5F1404%7EADC%5FZ%5F1406%23000000%7Eadc%5Fz%5F1406%7EADC%5FZ%5F1407%2381C8F2%7Eadc%5Fz%5F1407%7EADC%5FZ%5F1409%23000000%7Eadc%5Fz%5F1409%7EADC%5FZ%5F1410%23DEEBF7%7Eadc%5Fz%5F1410%7EADC%5FZ%5F1413GrayBlack%2F%7Eadc%5Fz%5F1413%7EADC%5FZ%5F1500A%7Eadc%5Fz%5F1500%7EADC%5FZ%5F1502N%7Eadc%5Fz%5F1502%7EADC%5FZ%5F1503TX%2F%7Eadc%5Fz%5F1503%7EADC%5FZ%5F1772TX%7Eadc%5Fz%5F1772%7EADC%5FZ%5F1773TXHO%7Eadc%5Fz%5F1773&G4=20240928115937&G3=10061&A1=T&G2=alex%40apartmentwolf%2Ecom&B1=75%2D812239%2D343463',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        # 'cookie': '_gid=GA1.2.1913137885.1727479579; __utmc=50201974; __utmz=50201974.1727521770.12.7.utmccn=(referral)|utmcsr=us.apartmentdata.com|utmcct=/|utmcmd=referral; ASPSESSIONIDCUATACSB=AMFIOCODNBAHAKAPNGJGIDGE; __utma=50201974.1315800874.1726249570.1727538170.1727542760.15; __utmb=50201974; _gat_gtag_UA_57735016_3=1; _ga=GA1.1.1315800874.1726249570; _ga_WGPY1JWDFK=GS1.1.1727542774.16.0.1727542780.0.0.0; ADS=G1=%7EADC%5FZ%5F100028%7Eadc%5Fz%5F1000%7EADC%5FZ%5F100120240928115944%7Eadc%5Fz%5F1001%7EADC%5FZ%5F10020%7Eadc%5Fz%5F1002%7EADC%5FZ%5F10070%7Eadc%5Fz%5F1007%7EADC%5FZ%5F10081%7Eadc%5Fz%5F1008%7EADC%5FZ%5F1009F%7Eadc%5Fz%5F1009%7EADC%5FZ%5F1010Y%7Eadc%5Fz%5F1010%7EADC%5FZ%5F1011N%7Eadc%5Fz%5F1011%7EADC%5FZ%5F101310061%7Eadc%5Fz%5F1013%7EADC%5FZ%5F10154291A%7Eadc%5Fz%5F1015%7EADC%5FZ%5F1016TX%7Eadc%5Fz%5F1016%7EADC%5FZ%5F1017TXHO%7Eadc%5Fz%5F1017%7EADC%5FZ%5F1018TXHO%7Eadc%5Fz%5F1018%7EADC%5FZ%5F10190%7Eadc%5Fz%5F1019%7EADC%5FZ%5F102099999%7Eadc%5Fz%5F1020%7EADC%5FZ%5F1021X%7Eadc%5Fz%5F1021%7EADC%5FZ%5F1022X%7Eadc%5Fz%5F1022%7EADC%5FZ%5F102310%7Eadc%5Fz%5F1023%7EADC%5FZ%5F1024HSVI%7Eadc%5Fz%5F1024%7EADC%5FZ%5F10251900%7Eadc%5Fz%5F1025%7EADC%5FZ%5F10269999%7Eadc%5Fz%5F1026%7EADC%5FZ%5F10271%7Eadc%5Fz%5F1027%7EADC%5FZ%5F10289999%7Eadc%5Fz%5F1028%7EADC%5FZ%5F10291%7Eadc%5Fz%5F1029%7EADC%5FZ%5F10309999%7Eadc%5Fz%5F1030%7EADC%5FZ%5F1034Y%7Eadc%5Fz%5F1034%7EADC%5FZ%5F10351%7Eadc%5Fz%5F1035%7EADC%5FZ%5F10360%7Eadc%5Fz%5F1036%7EADC%5FZ%5F10370%7Eadc%5Fz%5F1037%7EADC%5FZ%5F10380%2E00%7Eadc%5Fz%5F1038%7EADC%5FZ%5F1050AR%7Eadc%5Fz%5F1050%7EADC%5FZ%5F105150%7Eadc%5Fz%5F1051%7EADC%5FZ%5F1053A%7Eadc%5Fz%5F1053%7EADC%5FZ%5F10571%7Eadc%5Fz%5F1057%7EADC%5FZ%5F11000%7Eadc%5Fz%5F1100%7EADC%5FZ%5F11020%7Eadc%5Fz%5F1102%7EADC%5FZ%5F11030%7Eadc%5Fz%5F1103%7EADC%5FZ%5F11045%7Eadc%5Fz%5F1104%7EADC%5FZ%5F11060%7Eadc%5Fz%5F1106%7EADC%5FZ%5F11070%7Eadc%5Fz%5F1107%7EADC%5FZ%5F11085%7Eadc%5Fz%5F1108%7EADC%5FZ%5F1109P%7Eadc%5Fz%5F1109%7EADC%5FZ%5F11220%7Eadc%5Fz%5F1122%7EADC%5FZ%5F11230%7Eadc%5Fz%5F1123%7EADC%5FZ%5F11245%7Eadc%5Fz%5F1124%7EADC%5FZ%5F11255%7Eadc%5Fz%5F1125%7EADC%5FZ%5F11265%7Eadc%5Fz%5F1126%7EADC%5FZ%5F11275%7Eadc%5Fz%5F1127%7EADC%5FZ%5F11280%7Eadc%5Fz%5F1128%7EADC%5FZ%5F11290%7Eadc%5Fz%5F1129%7EADC%5FZ%5F120063939%7Eadc%5Fz%5F1200%7EADC%5FZ%5F12013863%7Eadc%5Fz%5F1201%7EADC%5FZ%5F1202Y%7Eadc%5Fz%5F1202%7EADC%5FZ%5F1205Y%7Eadc%5Fz%5F1205%7EADC%5FZ%5F1207ReLoad%7Eadc%5Fz%5F1207%7EADC%5FZ%5F1220147%7Eadc%5Fz%5F1220%7EADC%5FZ%5F122120240928115940%7Eadc%5Fz%5F1221%7EADC%5FZ%5F1230151%7Eadc%5Fz%5F1230%7EADC%5FZ%5F123120240928115939%7Eadc%5Fz%5F1231%7EADC%5FZ%5F1232Y%7Eadc%5Fz%5F1232%7EADC%5FZ%5F1233TXHO%7Eadc%5Fz%5F1233%7EADC%5FZ%5F1236Y%3A%7Eadc%5Fz%5F1236%7EADC%5FZ%5F1237N%7Eadc%5Fz%5F1237%7EADC%5FZ%5F123809%2F26%2F2024%7Eadc%5Fz%5F1238%7EADC%5FZ%5F1251Apartment+Wolf%7Eadc%5Fz%5F1251%7EADC%5FZ%5F125211906+Marrs+Dr%7Eadc%5Fz%5F1252%7EADC%5FZ%5F1254Houston%7Eadc%5Fz%5F1254%7EADC%5FZ%5F1255TX%7Eadc%5Fz%5F1255%7EADC%5FZ%5F125677065%7Eadc%5Fz%5F1256%7EADC%5FZ%5F1257281%2F701%2D0336%7Eadc%5Fz%5F1257%7EADC%5FZ%5F1260210%2F540%2D1552%7Eadc%5Fz%5F1260%7EADC%5FZ%5F1262http%3A%2F%2Fwww%2EApartmentWolf%2Ecom%7Eadc%5Fz%5F1262%7EADC%5FZ%5F1268%5EI1830%5Ei18%5EI19Basic%5Ei19%7Eadc%5Fz%5F1268%7EADC%5FZ%5F130063939%7Eadc%5Fz%5F1300%7EADC%5FZ%5F1301Alex%7Eadc%5Fz%5F1301%7EADC%5FZ%5F1302Taylor%7Eadc%5Fz%5F1302%7EADC%5FZ%5F1303281%2F701%2D0336%7Eadc%5Fz%5F1303%7EADC%5FZ%5F1306alex%40apartmentwolf%2Ecom%7Eadc%5Fz%5F1306%7EADC%5FZ%5F1307TX%5F613630%7Eadc%5Fz%5F1307%7EADC%5FZ%5F1400ADC%5FDefault%2Egif%7Eadc%5Fz%5F1400%7EADC%5FZ%5F1403%23000000%7Eadc%5Fz%5F1403%7EADC%5FZ%5F1404%23FFFFFF%7Eadc%5Fz%5F1404%7EADC%5FZ%5F1406%23000000%7Eadc%5Fz%5F1406%7EADC%5FZ%5F1407%2381C8F2%7Eadc%5Fz%5F1407%7EADC%5FZ%5F1409%23000000%7Eadc%5Fz%5F1409%7EADC%5FZ%5F1410%23DEEBF7%7Eadc%5Fz%5F1410%7EADC%5FZ%5F1413GrayBlack%2F%7Eadc%5Fz%5F1413%7EADC%5FZ%5F1500A%7Eadc%5Fz%5F1500%7EADC%5FZ%5F1502N%7Eadc%5Fz%5F1502%7EADC%5FZ%5F1503TX%2F%7Eadc%5Fz%5F1503%7EADC%5FZ%5F1772TX%7Eadc%5Fz%5F1772%7EADC%5FZ%5F1773TXHO%7Eadc%5Fz%5F1773&G4=20240928115937&G3=10061&A1=T&G2=alex%40apartmentwolf%2Ecom&B1=75%2D812239%2D343463',
        'priority': 'u=0, i',
        'referer': 'https://www.apartmentdata.com/EXERequest/ADC_ShowTop.asp?CLEAROPTIONS=Y&VIP=010',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }
    params = {
        'MODE': str(apartment_id),
        'MODE2': 'StartFromTop_Directory',
        'VIP': '010',
    }

    response = requests.get(
        'https://www.apartmentdata.com/EXERequest/ADC_ShowEBrochure.asp',
        params=params,
        cookies=cookies,
        headers=headers,
        timeout=2
    )

    # print(response.content)

    soup = BeautifulSoup(response.content, 'html.parser')


    # Find the first <font> tag that contains "ID:", safely checking for None
    font_with_id = soup.find('font', string=lambda text: text and 'ID:' in text)
    apartment_id=None
    # Get the next sibling of the found element and extract its text
    if font_with_id and font_with_id.next_sibling:
        apartment_id = font_with_id.next_sibling.strip()  # Strip to remove extra whitespace
        # print("Apartment ID:", apartment_id)
    else:
        print("Apartment ID not found.")



    # Find the first <font> tag inside the specified <div>
    apartment_title = soup.select_one('div.AptFont2Margin font font:first-child')

    # Extract and trim the text
    if apartment_title:
        apartments_title = apartment_title.get_text(strip=True)  # Using get_text() with strip=True to trim whitespace
        # print("Apartment Title:", apartments_title)
    else:
        print("Apartment Title not found.")



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
    else:
        print("Apartment address not found.")




    # Find the font element that contains "#Flrs:"
    total_number_of_floors_font = soup.select_one('div.AptFontMargin font:-soup-contains("#Flrs:") font:nth-of-type(3)')

    # Get the next sibling of the found element and extract its text
    if total_number_of_floors_font and total_number_of_floors_font.next_sibling:
        total_number_of_floors = total_number_of_floors_font.next_sibling.strip()  # Strip to remove extra whitespace
        # print("Total Number of floors:", total_number_of_floors)
    else:
        print("Total Number of floors not found.")



    # Find the font element that contains "Units:"
    total_number_of_units_font = soup.select_one('div.AptFontMargin font:-soup-contains("Units:") font:nth-of-type(2)')

    # Get the next sibling of the found element and extract its text
    if total_number_of_units_font and total_number_of_units_font.next_sibling:
        total_number_of_units = total_number_of_units_font.next_sibling.strip()  # Strip to remove extra whitespace
        # print("Total Number of units:", total_number_of_units)
    else:
        print("Total Number of units not found.")




    # Extracting the map number
    map_number_font = soup.select_one('div.AptFontMargin font:-soup-contains("Map#:") font:nth-of-type(4)')

    if map_number_font and map_number_font.next_sibling:
        map_number = map_number_font.next_sibling.strip()  # Strip to remove extra whitespace
        # print("Map Number:", map_number)
    else:
        print("Map Number not found.")


    # Extracting the CR number
    cr_number_font = soup.select_one('div.AptFontMargin font:-soup-contains("CR:") font:nth-of-type(5) font')

    if cr_number_font and cr_number_font.next_sibling:
        cr_number = cr_number_font.next_sibling.strip()  # Strip to remove extra whitespace
        # print("CR Number:", cr_number)
    else:
        print("CR Number not found.")



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

            # Print the extracted parameters
            # print("Mode:", mode)
            # print("Map Width:", map_width)
            # print("Map Height:", map_height)
            # print("Center Latitude:", map_center_lat)
            # print("Center Longitude:", map_center_lng)
            # print("Point Latitude:", map_point_lat)
            # print("Point Longitude:", map_point_lng)
            # print("Zoom Level:", map_zoom_level)
            # print("Use Point Info:", map_use_point_info)
            # print("Use Map Click:", map_use_map_click)
            # print("Use Address:", map_use_address)

            # Create a CSV file to write data
            # filename = 'apartment_data.csv'
            # Write to CSV file
        # csv_file = "location_details.csv"
            with open(csv_filepath,  mode='a', newline='', encoding='utf-8') as file:
            # writer = csv.DictWriter(file, fieldnames=headers)
            # writer.writeheader()  # Write headers
                writer = csv.writer(file)
                # writer.writerow(row)  # Write the single row with JSON formatted fields
            # with open(filename, mode='w', newline='') as file:
                # writer = csv.DictWriter(file, fieldnames=[
                #     "real_estate_property_identity",
                #     "Title",
                #     "Province / State",
                #     "City / Town",
                #     "real_estate_property_price_short",
                #     "real_estate_second-price",
                #     "real_estate_property_size",
                #     "real_estate_second-size",
                #     "real_estate_property_bedrooms",
                #     "real_estate_second-bedroom",
                #     "real_estate_property_bathrooms",
                #     "real_estate_second-bathroom",
                #     "real_estate_property_address",
                #     "real_estate_property_zip",
                #     "Floor Plans_floor_name",
                #     "Floor Plans_floor_price",
                #     "Floor Plans_floor_size",
                #     "Floor Plans_bedroom",
                #     "Floor Plans_bathroom",
                #     "Extra Address Field",
                #     "Extra Latitude Field"
                # ])
                
                # # Write the header
                # # writer.writeheader()
                
                # Prepare the data
                # print(bedroom_price_string[-1])
                # print(bedroom_price_string.split("-")[1].replace('$', '').replace(',', '') if len(bedroom_price_string) > 1 else bedroom_price_string[-1].replace('$', '').replace(',', ''))
                # print("bedroom_price_string : ", bedroom_price_string.split("|")[0].replace('$', '').replace(',', '') )
                # print(bedroom_price_string)
                # print("real_estate_property_price_short : ",bedroom_price_string.split("|")[0].split("-")[0].replace('$', '').replace(',', '') )
                # print("real_estate_second-price : ",bedroom_price_string.split("|")[-1].split("-")[-1].replace('$', '').replace(',', '') )
                # print("real_estate_property_size : ", bedroom_size_string.split("|")[0].split("-")[0].replace('$', '').replace(',', ''))
                # print("real_estate_second-size : ", bedroom_size_string.split("|")[-1].split("-")[-1].replace('$', '').replace(',', ''))
                # print("real_estate_property_bedrooms : ", plans_bedroom_string.split("|")[0])
                # print("real_estate_second-bedroom : ", plans_bedroom_string.split("|")[-1])
                # print("real_estate_property_bathrooms : ", plans_bathroom_string.split("|")[0])
                # print("real_estate_second-bathroom : ", plans_bathroom_string.split("|")[0])
                # print("real_estate_property_address : ", apartment_address_value)
                # print("real_estate_property_zip : ", state_and_zip[-1])
                # # print("Plans_floor_price : ",  )
                # print("Plans_floor_price : ",  '|'.join([price.split('-')[0].replace('$', '').replace(',', '') for price in bedroom_price_string.split("|")]))
                # print("Floor Plans_floor_size : ",  '|'.join([size.split("-")[0].replace(",", "") for size in bedroom_size_string.split("|")]))
                # print("Floor Plans_bedroom : ",  plans_bedroom_string)
                # print("Floor Plans_bathroom : ",  plans_bathroom_string)
                # print("Extra Address Field : ",  apartment_address_value)
                # print("Extra Latitude Field : ",  f"{map_point_lat},{map_point_lng}")
                data = {
                    "real_estate_property_identity": apartment_id,
                    "Title": apartments_title,
                    # "Province / State": state_and_zip,
                    "Province / State": state_and_zip[0],
                    "City / Town": city,
                    # "real_estate_property_price_short": bedroom_price_string.split("|")[0].replace('$', '').replace(',', '') ,
                    "real_estate_property_price_short": bedroom_price_string.split("|")[0].split("-")[0].replace('$', '').replace(',', '') ,
                    "real_estate_second-price": bedroom_price_string.split("|")[-1].split("-")[-1].replace('$', '').replace(',', '') ,
                    "real_estate_property_size": bedroom_size_string.split("|")[0].split("-")[0].replace('$', '').replace(',', ''),  # Assuming sizes are formatted correctly
                    "real_estate_second-size": bedroom_size_string.split("|")[-1].split("-")[-1].replace('$', '').replace(',', ''),
                    "real_estate_property_bedrooms": plans_bedroom_string.split("|")[0],
                    "real_estate_second-bedroom": plans_bedroom_string.split("|")[-1],
                    "real_estate_property_bathrooms": plans_bathroom_string.split("|")[0],
                    "real_estate_second-bathroom": plans_bathroom_string.split("|")[-1],
                    "real_estate_property_address": apartment_address_value,
                    "real_estate_property_zip": state_and_zip[-1],
                    "Floor Plans_floor_name": bedroom_plan_string,
                    # "Floor Plans_floor_price": '|'.join([price.split('-')[0].replace('$', '').replace(',', '') for price in bedroom_price_string]),
                    "Floor Plans_floor_price": '|'.join([price.split('-')[0].replace('$', '').replace(',', '') for price in bedroom_price_string.split("|")]),
                    "Floor Plans_floor_size": '|'.join([size.split("-")[0].replace(",", "") for size in bedroom_size_string.split("|")]),
                    # "Floor Plans_bedroom": '|'.join(map(str, plans_bedroom_string)),
                    "Floor Plans_bedroom": plans_bedroom_string,
                    # "Floor Plans_bathroom": '|'.join(map(str, plans_bathroom_string)),
                    "Floor Plans_bathroom": plans_bathroom_string,
                    "Extra Address Field": apartment_address_value,
                    "Extra Latitude Field": f"{map_point_lat},{map_point_lng}"
                }
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
                
                        # Write the data
                writer.writerow(data)

            # print(f"Data written to {csv_filepath}")
        else:
            print("URL not found in script content.")
    else:
        print("Script content with ShowMap_EBrochure not found.")
