import requests

cookies = {
    'grav-site-d7e546baa1f86ac060dcd060a7000547': '0pamt0pkdhi0bfatd7rputttcs',
    'adata-pa-types-v2': 'eyJwb3RlbnRpYWwiOjEsImNvbXBzIjoxLCJvcHRpb25hbF9maWx0ZXIiOjB9',
    '_gid': 'GA1.2.1972150433.1727557319',
    '__utmc': '50201974',
    '__utmz': '50201974.1727557336.7.4.utmccn=(referral)|utmcsr=us.apartmentdata.com|utmcct=/|utmcmd=referral',
    '__utma': '50201974.1801150827.1724878151.1727557336.1727562721.8',
    '__utmb': '50201974',
    '_ga_WGPY1JWDFK': 'GS1.1.1727563139.9.0.1727563139.0.0.0',
    '_ga': 'GA1.2.1294934402.1724878135',
    '_gat_gtag_UA_57735016_3': '1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ur;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'grav-site-d7e546baa1f86ac060dcd060a7000547=0pamt0pkdhi0bfatd7rputttcs; adata-pa-types-v2=eyJwb3RlbnRpYWwiOjEsImNvbXBzIjoxLCJvcHRpb25hbF9maWx0ZXIiOjB9; _gid=GA1.2.1972150433.1727557319; __utmc=50201974; __utmz=50201974.1727557336.7.4.utmccn=(referral)|utmcsr=us.apartmentdata.com|utmcct=/|utmcmd=referral; __utma=50201974.1801150827.1724878151.1727557336.1727562721.8; __utmb=50201974; _ga_WGPY1JWDFK=GS1.1.1727563139.9.0.1727563139.0.0.0; _ga=GA1.2.1294934402.1724878135; _gat_gtag_UA_57735016_3=1',
    'origin': 'https://us.apartmentdata.com',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': 'https://us.apartmentdata.com/login',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

data = {
    'MS_LogIn_User': 'alex@apartmentwolf.com',
    'MS_LogIn_Password': '386349',
    'MS_Login_Type': 'L',
    'task': 'login.login',
    'login-form-nonce': '7c6b038c529b668931f7c2f0c015d803',
}

response = requests.post('https://us.apartmentdata.com/login', cookies=cookies, headers=headers, data=data)

print(response.content)