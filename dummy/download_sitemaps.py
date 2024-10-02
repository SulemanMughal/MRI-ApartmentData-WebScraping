import requests
import xml.etree.ElementTree as ET
import csv

# Function to download and parse the sitemap
def download_sitemap(sitemap_url):
    # Download sitemap XML content
    response = requests.get(sitemap_url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve sitemap: {response.status_code}")
        return None

# Function to parse sitemap and extract URLs
def parse_sitemap(sitemap_content):
    urls = []
    root = ET.fromstring(sitemap_content)
    for url in root.findall("{http://www.google.com/schemas/sitemap/0.84}url"):
        loc = url.find("{http://www.google.com/schemas/sitemap/0.84}loc").text
        urls.append(loc)
    return urls

# Function to save URLs to a CSV file
def save_to_csv(urls, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["URL"])  # Write header
        for url in urls:
            writer.writerow([url])  # Write URL in each row

# Main logic
sitemap_url = 'http://www.apartmentdata.com/sitemap.xml'  # Replace with your sitemap URL
sitemap_content = download_sitemap(sitemap_url)

if sitemap_content:
    urls = parse_sitemap(sitemap_content)
    save_to_csv(urls, 'urls.csv')
    print(f"Saved {len(urls)} URLs to urls.csv")
