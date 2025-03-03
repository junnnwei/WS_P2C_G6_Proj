from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Sample data for forms
data = {
    "login": {"email": "test@example.com", "password": "password123"},
    "registration": {"name": "John Doe", "email": "johndoe@example.com", "password": "SecurePass123", "cpassword": "SecurePass123"},
    "payment": {"card-name": "John Doe", "card-number": "4111111111111111", "expiry": "12/25", "cvv": "123"},
    "feedback": {"feedback-type": "comments", "message": "Amazing service!", "name": "John Doe", "email": "johndoe@example.com"}
}

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def fill_login_form():
    driver.get("http://35.212.185.236/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    
    for _ in range(250):
        driver.find_element(By.ID, "email").send_keys(data["login"]["email"])
        driver.find_element(By.ID, "password").send_keys(data["login"]["password"])
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)

def fill_registration_form():
    driver.get("http://127.0.0.1:5000/registration")
    for _ in range(250):
        driver.find_element(By.ID, "name").send_keys(data["registration"]["name"])
        driver.find_element(By.ID, "email").send_keys(data["registration"]["email"])
        driver.find_element(By.ID, "password").send_keys(data["registration"]["password"])
        driver.find_element(By.ID, "cpassword").send_keys(data["registration"]["cpassword"])
        terms_checkbox = driver.find_element(By.ID, "termsandconditions")
        if not terms_checkbox.is_selected():
            terms_checkbox.click()
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)

def fill_payment_form():
    driver.get("http://127.0.0.1:5000/payment")
    for _ in range(250):
        driver.find_element(By.ID, "card-name").send_keys(data["payment"]["card-name"])
        driver.find_element(By.ID, "card-number").send_keys(data["payment"]["card-number"])
        driver.find_element(By.ID, "expiry").send_keys(data["payment"]["expiry"])
        driver.find_element(By.ID, "cvv").send_keys(data["payment"]["cvv"])
        driver.find_element(By.CLASS_NAME, "button").click()
        time.sleep(2)

def fill_feedback_form():
    driver.get("http://127.0.0.1:5000/feedback")
    for _ in range(250):
        feedback_type = data["feedback"]["feedback-type"]
        feedback_radio = driver.find_element(By.ID, feedback_type)
        if not feedback_radio.is_selected():
            feedback_radio.click()
        driver.find_element(By.ID, "message").send_keys(data["feedback"]["message"])
        driver.find_element(By.ID, "name").send_keys(data["feedback"]["name"])
        driver.find_element(By.ID, "email").send_keys(data["feedback"]["email"])
        driver.find_element(By.CLASS_NAME, "button").click()
        time.sleep(2)

# Run all form filling functions
fill_login_form()
# fill_registration_form()
# fill_payment_form()
# fill_feedback_form()

driver.quit()
