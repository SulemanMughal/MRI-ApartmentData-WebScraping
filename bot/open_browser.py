from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import urllib.parse



# Example Python function to receive cookies, params, and headers
def process_request(cookies, params, headers):
    print("Cookies:", cookies)
    print("URL Parameters:", params)
    print("Headers:", headers)

def get_response(target_url):

    # Initialize Chrome driver (ChromeDriver must be in your system's PATH)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Optional: Uncomment for headless mode

    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL
    # url = "http://www.apartmentdata.com/apartment-search/channelview-apartments.asp"
    url = target_url
    driver.get(url)


    # Click on the first button with 'onclick' attribute
    # first_button = driver.find_element(By.XPATH, "//a[@onclick='FormActionSubmit(\"Next\",\"0\",\"TXHO\",\"ChannelviewR08\");']")
    # first_button.click()

    # Select the anchor tag with onclick attribute that starts with 'FormActionSubmit'
    button = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td/font/form/table[1]/tbody/tr/td[3]/table[1]/tbody/tr[2]/td/div/a")
    button.click()


    # Wait for the page to load (adjust sleep if needed for your use case)
    time.sleep(3)

    # Click on the "Accept All Cookies" button
    try:
        accept_cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        accept_cookies_button.click()
        print("Accepted all cookies.")
    except Exception as e:
        print(f"Accept Cookies button not found: {e}")

    # # Now click on the "Login" link by href
    # login_button = driver.find_element(By.XPATH, "//a[@href='https://us.apartmentdata.com/login']")
    # login_button.click()


    # # Perform further actions or close the browser if needed
    # print("All buttons clicked successfully!")


    # Open the login URL directly
    url = "https://us.apartmentdata.com/login"
    driver.get(url)

    # Perform actions on the login page if necessary
    # Example: Filling out login credentials (if login form is available)
    # username_field = driver.find_element(By.NAME, "username")  # Modify as per actual element name or id
    # password_field = driver.find_element(By.NAME, "password")  # Modify as per actual element name or id
    # username_field.send_keys("your_username")
    # password_field.send_keys("your_password")

    # Click login button (modify selector as needed)
    # login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    # login_button.click()

    # Print confirmation
    print("Login page opened successfully!")

    # Close the browser
    time.sleep(5)  # Adjust based on the actions being performed

    # Close the browser
    # driver.quit()


    # Fill in the email field
    try:
        email_field = driver.find_element(By.ID, "MS_LogIn_User")
        email_field.send_keys("alex@apartmentwolf.com")  # Replace with your email or test data
        print("Email entered successfully!")
    except Exception as e:
        print(f"Error locating the email field: {e}")



    # Fill in the password field
    try:
        password_field = driver.find_element(By.ID, "MS_LogIn_Password")
        password_field.send_keys("386349")  # Replace with the actual password
        print("Password entered successfully!")
    except Exception as e:
        print(f"Error locating the password field: {e}")

    time.sleep(3)

    # Click the login button
    try:
        login_button = driver.find_element(By.XPATH, "//button[@name='task' and @value='login.login']")
        login_button.click()
        print("Login button clicked successfully!")
    except Exception as e:
        print(f"Error clicking the login button: {e}")


    time.sleep(5)


    try:
        full_search_btn = driver.find_element(
            By.XPATH, "/html/body/table/tbody/tr[2]/td/font/form/table/tbody/tr/td[2]/table[3]/tbody/tr[3]/td[2]/table[2]/tbody/tr[1]/td[1]/div/a"
        )
        full_search_btn.click()
        print("Full search button click")

        time.sleep(5)

    except Exception as e:
        print(f"Error clicking the Full search button: {e}")


    # Retrieve cookies from the browser
    cookies = driver.get_cookies()  # This returns a list of dictionaries representing cookies

    # Parse URL parameters from the current URL
    current_url = driver.current_url
    parsed_url = urllib.parse.urlparse(current_url)
    params = urllib.parse.parse_qs(parsed_url.query)  # Returns a dictionary of query parameters

    # Set headers manually (since Selenium can't access HTTP headers directly)
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

    driver.quit()

    # Pass cookies, params, and headers to the function
    # return process_request(cookies, params, headers)
    return (cookies, params, headers)


    # while True:
    #     print("---")

