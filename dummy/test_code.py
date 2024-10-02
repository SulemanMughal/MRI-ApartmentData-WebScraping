import requests

# Define the URL and modify the region by changing the VIP parameter
url = 'https://www.apartmentdata.com/EXERequest/ADC_ShowResults.asp?SHOWPAGE=1&VIP={}'

# Change this to any region code you want to test (e.g., 001 for a different region)
region_code = '001'

# Define the headers (same as your curl request)
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ur;q=0.8',
    'cache-control': 'no-cache',
    'cookie': '_gid=GA1.2.1972150433.1727557319; __utmc=50201974; __utmz=50201974.1727557336.7.4.utmccn=(referral)|utmcsr=us.apartmentdata.com|utmcct=/|utmcmd=referral; ASPSESSIONIDCUATACSB=ACOIOCODKNKADJMDKPDEGMHF; __utma=50201974.1801150827.1724878151.1727557336.1727562721.8; __utmb=50201974; _ga=GA1.2.1294934402.1724878135; _gat_gtag_UA_57735016_3=1',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://www.apartmentdata.com/EXERequest/ADC_ShowLocTools.asp?MODE=StartFromTop&SAVE=Y&VIP=000',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

# Send the request with the modified region code
response = requests.get(url.format(region_code), headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the first 500 characters of the response
    print("Response:", response.text[:500])
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
