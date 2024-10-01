import chromedriver_autoinstaller
from pyvirtualdisplay import Display
from selenium import webdriver

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")  # Required when running as root
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")

# Start a virtual display
with Display(visible=0, size=[800, 600]) as display:
    
    # install chrome driver
    chromedriver_autoinstaller.install()

    # Create a Selenium WebDriver with the virtual display
    driver = webdriver.Chrome(options=chrome_options)

    # Now you can use the WebDriver to interact with a web page
    driver.get("https://www.google.com")
    print(driver.title)
  
    # Close the WebDriver when done
    driver.quit()
