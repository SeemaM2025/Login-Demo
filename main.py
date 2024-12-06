from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time, json

# Define locators for both websites
locators = {
    'saucedemo': {
        'username': (By.ID, 'user-name'),
        'password': (By.ID, 'password'),
        'login_button': (By.ID, 'login-button'),
        'welcome_header': (By.XPATH, '//div[contains(text(), "Swag Labs")]'),
    },
    'practice_automation': {
        'username': (By.ID, 'username'),
        'password': (By.ID, 'password'),
        'login_button': (By.ID, 'submit'),
        'welcome_header': (By.XPATH, "//h1[text()='Logged In Successfully']"),
    }
}

# Read credentials from JSON file
def read_credentials(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Perform login and validation
def login_and_validate(driver, url, locators, username, password, screenshot_path):
    print(f"Navigating to {url}...")
    driver.get(url)  # Navigate to the website
    time.sleep(2)  # Pause to observe the browser loading

    wait = WebDriverWait(driver, 20, poll_frequency=1)  # Explicit wait with a timeout of 20 seconds

    # Enter username
    user_elem = wait.until(EC.visibility_of_element_located(locators['username']))
    print("Entering username...")
    user_elem.send_keys(username)
    time.sleep(1)  # Pause to observe the username being entered

    # Enter password
    pass_elem = wait.until(EC.visibility_of_element_located(locators['password']))
    print("Entering password...")
    pass_elem.send_keys(password)
    time.sleep(1)  # Pause to observe the password being entered

    # Click login button
    login_button = wait.until(EC.visibility_of_element_located(locators['login_button']))
    print("Clicking login button...")
    login_button.click()
    time.sleep(2)  # Pause to observe the login action

    # Verify successful login
    success_elem = wait.until(EC.visibility_of_element_located(locators['welcome_header']))
    if success_elem:
        print("Login successful!")
        driver.save_screenshot(screenshot_path)  # Take a screenshot of the successful login
        print(f"Screenshot saved at {screenshot_path}")
    time.sleep(3)  # Pause to observe the logged-in page

# Main execution
def main():
    # Initialize WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Load credentials
    credentials = read_credentials('assets/credentials.json')

    # Login to the first site
    print("Logging into SauceDemo...")
    login_and_validate(
        driver,
        url='https://www.saucedemo.com',
        locators=locators['saucedemo'],
        username=credentials['saucedemo_username'],
        password=credentials['saucedemo_password'],
        screenshot_path='./snapshots/Login_successful_Saucedemo.png'
    )

    # Login to the second site
    print("Logging into Practice Automation...")
    login_and_validate(
        driver,
        url='https://practicetestautomation.com/practice-test-login/',
        locators=locators['practice_automation'],
        username=credentials['practice_automation_username'],
        password=credentials['practice_automation_password'],
        screenshot_path='./snapshots/Login_successful_practice_automation.png'
    )

    # Close the browser
    print("Closing the browser...")
    time.sleep(5)  # Pause to observe before closing the browser
    driver.quit()

if __name__ == "__main__":
    main()
