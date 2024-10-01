import chromedriver_autoinstaller
from pyvirtualdisplay import Display
from selenium import webdriver

# Start a virtual display
with Display(visible=0, size=[800, 600]) as display:
    
    # install chrome driver
    chromedriver_autoinstaller.install()

    # Create a Selenium WebDriver with the virtual display
    driver = webdriver.Chrome()

    # Now you can use the WebDriver to interact with a web page
    driver.get("https://www.google.com")
    print(driver.title)
  
    # Close the WebDriver when done
    driver.quit()