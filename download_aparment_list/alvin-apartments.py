import requests
# import requests
from bs4 import BeautifulSoup

import re

import time

import csv


output_file_path = "alvin-apartments.csv"

with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=[
        "id"
    ])
    writer.writeheader()  

cookies = {
    '_gid': 'GA1.2.1972150433.1727557319',
    '__utmc': '50201974',
    '__utmz': '50201974.1727557336.7.4.utmccn=(referral)|utmcsr=us.apartmentdata.com|utmcct=/|utmcmd=referral',
    'ASPSESSIONIDCUATACSB': 'ACOIOCODKNKADJMDKPDEGMHF',
    '__utma': '50201974.1801150827.1724878151.1727557336.1727562721.8',
    '__utmb': '50201974',
    '_ga': 'GA1.2.1294934402.1724878135',
    '_gat_gtag_UA_57735016_3': '1',
    'ADS': 'G1=%7EADC%5FZ%5F100028%7Eadc%5Fz%5F1000%7EADC%5FZ%5F100120240928180337%7Eadc%5Fz%5F1001%7EADC%5FZ%5F10020%7Eadc%5Fz%5F1002%7EADC%5FZ%5F10070%7Eadc%5Fz%5F1007%7EADC%5FZ%5F10080%7Eadc%5Fz%5F1008%7EADC%5FZ%5F1009F%7Eadc%5Fz%5F1009%7EADC%5FZ%5F1010Y%7Eadc%5Fz%5F1010%7EADC%5FZ%5F1011N%7Eadc%5Fz%5F1011%7EADC%5FZ%5F101310061%7Eadc%5Fz%5F1013%7EADC%5FZ%5F10150%7Eadc%5Fz%5F1015%7EADC%5FZ%5F1017TXHO%7Eadc%5Fz%5F1017%7EADC%5FZ%5F1018TXHO%7Eadc%5Fz%5F1018%7EADC%5FZ%5F10190%7Eadc%5Fz%5F1019%7EADC%5FZ%5F102099999%7Eadc%5Fz%5F1020%7EADC%5FZ%5F1021X%7Eadc%5Fz%5F1021%7EADC%5FZ%5F1022X%7Eadc%5Fz%5F1022%7EADC%5FZ%5F102310%7Eadc%5Fz%5F1023%7EADC%5FZ%5F1024HSVI%7Eadc%5Fz%5F1024%7EADC%5FZ%5F10251900%7Eadc%5Fz%5F1025%7EADC%5FZ%5F10269999%7Eadc%5Fz%5F1026%7EADC%5FZ%5F10271%7Eadc%5Fz%5F1027%7EADC%5FZ%5F10289999%7Eadc%5Fz%5F1028%7EADC%5FZ%5F10291%7Eadc%5Fz%5F1029%7EADC%5FZ%5F10309999%7Eadc%5Fz%5F1030%7EADC%5FZ%5F1034Y%7Eadc%5Fz%5F1034%7EADC%5FZ%5F10350%7Eadc%5Fz%5F1035%7EADC%5FZ%5F10360%7Eadc%5Fz%5F1036%7EADC%5FZ%5F10370%7Eadc%5Fz%5F1037%7EADC%5FZ%5F10380%2E00%7Eadc%5Fz%5F1038%7EADC%5FZ%5F1050AR%7Eadc%5Fz%5F1050%7EADC%5FZ%5F105150%7Eadc%5Fz%5F1051%7EADC%5FZ%5F1053A%7Eadc%5Fz%5F1053%7EADC%5FZ%5F10570%7Eadc%5Fz%5F1057%7EADC%5FZ%5F11001%7Eadc%5Fz%5F1100%7EADC%5FZ%5F1101Alvin%7Eadc%5Fz%5F1101%7EADC%5FZ%5F110229%2E427228%7Eadc%5Fz%5F1102%7EADC%5FZ%5F1103%2D95%2E225373%7Eadc%5Fz%5F1103%7EADC%5FZ%5F110412%7Eadc%5Fz%5F1104%7EADC%5FZ%5F11060%7Eadc%5Fz%5F1106%7EADC%5FZ%5F11070%7Eadc%5Fz%5F1107%7EADC%5FZ%5F11085%7Eadc%5Fz%5F1108%7EADC%5FZ%5F1109P%7Eadc%5Fz%5F1109%7EADC%5FZ%5F11220%7Eadc%5Fz%5F1122%7EADC%5FZ%5F11230%7Eadc%5Fz%5F1123%7EADC%5FZ%5F11245%7Eadc%5Fz%5F1124%7EADC%5FZ%5F11255%7Eadc%5Fz%5F1125%7EADC%5FZ%5F11265%7Eadc%5Fz%5F1126%7EADC%5FZ%5F11275%7Eadc%5Fz%5F1127%7EADC%5FZ%5F11280%7Eadc%5Fz%5F1128%7EADC%5FZ%5F11290%7Eadc%5Fz%5F1129%7EADC%5FZ%5F120010061%7Eadc%5Fz%5F1200%7EADC%5FZ%5F1202Y%7Eadc%5Fz%5F1202%7EADC%5FZ%5F1205Y%7Eadc%5Fz%5F1205%7EADC%5FZ%5F1207ReLoad%7Eadc%5Fz%5F1207%7EADC%5FZ%5F1232N%7Eadc%5Fz%5F1232%7EADC%5FZ%5F1233TXHO%7Eadc%5Fz%5F1233%7EADC%5FZ%5F1236N%3A%7Eadc%5Fz%5F1236%7EADC%5FZ%5F1237N%7Eadc%5Fz%5F1237%7EADC%5FZ%5F1250Z1100%7Eadc%5Fz%5F1250%7EADC%5FZ%5F1251ApartmentData%2Ecom%7Eadc%5Fz%5F1251%7EADC%5FZ%5F12522550+Gray+Falls%2C+Suite+450%7Eadc%5Fz%5F1252%7EADC%5FZ%5F1254Houston%7Eadc%5Fz%5F1254%7EADC%5FZ%5F1255TX%7Eadc%5Fz%5F1255%7EADC%5FZ%5F125677077%7Eadc%5Fz%5F1256%7EADC%5FZ%5F1257281%2F759%2D2200%7Eadc%5Fz%5F1257%7EADC%5FZ%5F1258800%2F595%2D8730%7Eadc%5Fz%5F1258%7EADC%5FZ%5F1260281%2F759%2D2210%7Eadc%5Fz%5F1260%7EADC%5FZ%5F1261800%2F790%2D4615%7Eadc%5Fz%5F1261%7EADC%5FZ%5F1262https%3A%2F%2Fwww%2EApartmentData%2Ecom%7Eadc%5Fz%5F1262%7EADC%5FZ%5F1400Z1100%5FADC%2Ejpg%7Eadc%5Fz%5F1400%7EADC%5FZ%5F1401Z1100%5FADC%5FX%2Egif%7Eadc%5Fz%5F1401%7EADC%5FZ%5F1403%23000000%7Eadc%5Fz%5F1403%7EADC%5FZ%5F1404%23FFFFFF%7Eadc%5Fz%5F1404%7EADC%5FZ%5F1406%23000000%7Eadc%5Fz%5F1406%7EADC%5FZ%5F1407%2381C8F2%7Eadc%5Fz%5F1407%7EADC%5FZ%5F1409%23000000%7Eadc%5Fz%5F1409%7EADC%5FZ%5F1410%23DEEBF7%7Eadc%5Fz%5F1410%7EADC%5FZ%5F1413ADC%2F%7Eadc%5Fz%5F1413%7EADC%5FZ%5F1500F%7Eadc%5Fz%5F1500%7EADC%5FZ%5F1502Y%7Eadc%5Fz%5F1502%7ELTSR%5FADC%5FZ%5F11000%7Eltsr%5Fadc%5Fz%5F1100%7ELTSR%5FADC%5FZ%5F11020%7Eltsr%5Fadc%5Fz%5F1102%7ELTSR%5FADC%5FZ%5F11030%7Eltsr%5Fadc%5Fz%5F1103%7ELTSR%5FADC%5FZ%5F11045%7Eltsr%5Fadc%5Fz%5F1104%7ELTSR%5FADC%5FZ%5F11060%7Eltsr%5Fadc%5Fz%5F1106%7ELTSR%5FADC%5FZ%5F11070%7Eltsr%5Fadc%5Fz%5F1107%7ELTSR%5FADC%5FZ%5F11085%7Eltsr%5Fadc%5Fz%5F1108%7ELTSR%5FADC%5FZ%5F1109P%7Eltsr%5Fadc%5Fz%5F1109%7ELTSR%5FADC%5FZ%5F11220%7Eltsr%5Fadc%5Fz%5F1122%7ELTSR%5FADC%5FZ%5F11230%7Eltsr%5Fadc%5Fz%5F1123%7ELTSR%5FADC%5FZ%5F11245%7Eltsr%5Fadc%5Fz%5F1124%7ELTSR%5FADC%5FZ%5F11255%7Eltsr%5Fadc%5Fz%5F1125%7ELTSR%5FADC%5FZ%5F11265%7Eltsr%5Fadc%5Fz%5F1126%7ELTSR%5FADC%5FZ%5F11275%7Eltsr%5Fadc%5Fz%5F1127%7ELTSR%5FADC%5FZ%5F11280%7Eltsr%5Fadc%5Fz%5F1128%7ELTSR%5FADC%5FZ%5F11290%7Eltsr%5Fadc%5Fz%5F1129&B1=16%2D432219%2D783545&G2=alex%40apartmentwolf%2Ecom&A1=T&G3=10061&G4=20240928180337',
    '_ga_WGPY1JWDFK': 'GS1.1.1727563139.9.1.1727564618.0.0.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ur;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://us.apartmentdata.com/',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

params = {
    'SHOWPAGE': '1',
    'VIP': '000',
}

url = 'https://www.apartmentdata.com/EXERequest/ADC_ShowResults.asp'


# # Function to save URLs to a CSV file
# def save_to_csv(urls, filename):
#     with open(filename, mode='a+', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(["URL"])  # Write header
#         for url in urls:
#             writer.writerow([url])  # Write URL in each row


response = requests.get(
    url,
    params=params,
    cookies=cookies,
    headers=headers,
)
response.raise_for_status()  # Check for successful request
soup = BeautifulSoup(response.content, 'html.parser')
anchors = soup.select('table.Apt2 a')
with open(output_file_path,  mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for anchor in anchors:
        href = anchor.get('name')  # Get the href attribute of the anchor
        if href:
            # print(f"Link: {href}")
            writer.writerow([href])



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
        cookies=cookies,
        headers=headers)
    response.raise_for_status()  # Check for successful request

    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags inside <table> tags with class "Apt2"
    # anchors = soup.select('table.Apt2 tbody tr td a')
    anchors = soup.select('table.Apt2 a')

    with open(output_file_path,  mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for anchor in anchors:
            href = anchor.get('name')  # Get the href attribute of the anchor
            if href:
                # print(f"Link: {href}")
                writer.writerow([href])
    # for anchor in anchors:
    #     href = anchor.get('name')
    #     if href:
    #         print(f"Link: {href}")
