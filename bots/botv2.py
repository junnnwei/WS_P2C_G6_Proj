from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Sample data for forms
data = {
    "login": {"email": "test@example.com", "password": "password123"},
    "registration": {"name": "John Doe", "email": "johndoe@example.com", "password": "SecurePass123", "cpassword": "SecurePass123"},
    "payment": {"card-name": "John Doe", "card-number": "4111111111111111", "expiry": "12/25", "cvv": "123"},
    "feedback": {"feedback-type": "comments", "message": "Amazing service!", "name": "John Doe", "email": "johndoe@example.com"}
}

# # Initialize ChromeDriver with random User-Agent
# user_agents = [
#     "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
#     "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0 BaiduSpider/2.0",
#     "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"
# ]

options = webdriver.ChromeOptions()
options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0 BaiduSpider/2.0")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

# def set_random_window_size(driver):
#     """Randomly resize the window to mimic different user behaviors."""
#     width = random.randint(300, 1000)
#     height = random.randint(300, 1000)
#     driver.set_window_size(width, height)
#     print(f"Window size set to {width}x{height}")

def slow_type(element, text):
    """Simulate typing with dynamic speed ranging from instant to super fast."""
    min_delay = random.uniform(0, 0.05)
    max_delay = random.uniform(min_delay, min_delay + 0.1)
    print(f"Typing speed range: {min_delay:.2f}s to {max_delay:.2f}s")

    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))

def fill_login_form():
    # for _ in range(250):
    #     # set_random_window_size(driver)
    #     driver.get("http://127.0.0.1:5000/")
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

        # email_input = driver.find_element(By.ID, "email")
        # password_input = driver.find_element(By.ID, "password")
        # submit_btn = driver.find_element(By.ID, "submit")

        # slow_type(email_input, data["login"]["email"])
        # slow_type(password_input, data["login"]["password"])

        # submit_btn.click()
        # time.sleep(random.uniform(1, 4))

    driver.get("http://127.0.0.1:5000/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    
    for _ in range(250):
        driver.find_element(By.ID, "email").send_keys(data["login"]["email"])
        driver.find_element(By.ID, "password").send_keys(data["login"]["password"])
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        

def fill_registration_form():
    # for _ in range(250):
    #     # set_random_window_size(driver)
    #     driver.get("http://127.0.0.1:5000/registration")

    #     slow_type(driver.find_element(By.ID, "name"), data["registration"]["name"])
    #     slow_type(driver.find_element(By.ID, "email"), data["registration"]["email"])
    #     slow_type(driver.find_element(By.ID, "password"), data["registration"]["password"])
    #     slow_type(driver.find_element(By.ID, "cpassword"), data["registration"]["cpassword"])

    #     terms_checkbox = driver.find_element(By.ID, "termsandconditions")
    #     if not terms_checkbox.is_selected():
    #         terms_checkbox.click()

    #     driver.find_element(By.ID, "submit").click()
    #     time.sleep(random.uniform(1, 4))
    driver.get("http://127.0.0.1:5000/registration")
    for _ in range(500):
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
    # for _ in range(250):
    #     # set_random_window_size(driver)
    #     driver.get("http://127.0.0.1:5000/payment")

    #     slow_type(driver.find_element(By.ID, "card-name"), data["payment"]["card-name"])
    #     slow_type(driver.find_element(By.ID, "card-number"), data["payment"]["card-number"])
    #     slow_type(driver.find_element(By.ID, "expiry"), data["payment"]["expiry"])
    #     slow_type(driver.find_element(By.ID, "cvv"), data["payment"]["cvv"])

    #     driver.find_element(By.CLASS_NAME, "button").click()
    #     time.sleep(random.uniform(1, 4))

    driver.get("http://127.0.0.1:5000/payment")
    for _ in range(500):
        driver.find_element(By.ID, "card-name").send_keys(data["payment"]["card-name"])
        driver.find_element(By.ID, "card-number").send_keys(data["payment"]["card-number"])
        driver.find_element(By.ID, "expiry").send_keys(data["payment"]["expiry"])
        driver.find_element(By.ID, "cvv").send_keys(data["payment"]["cvv"])
        driver.find_element(By.CLASS_NAME, "button").click()
        time.sleep(2)

def fill_feedback_form():
    # for _ in range(250):
    #     # set_random_window_size(driver)
    #     driver.get("http://127.0.0.1:5000/feedback")

    #     feedback_type = data["feedback"]["feedback-type"]
    #     feedback_radio = driver.find_element(By.ID, feedback_type)
    #     if not feedback_radio.is_selected():
    #         feedback_radio.click()

    #     slow_type(driver.find_element(By.ID, "message"), data["feedback"]["message"])
    #     slow_type(driver.find_element(By.ID, "name"), data["feedback"]["name"])
    #     slow_type(driver.find_element(By.ID, "email"), data["feedback"]["email"])

    #     driver.find_element(By.CLASS_NAME, "button").click()
    #     time.sleep(random.uniform(1, 4))
    driver.get("http://127.0.0.1:5000/feedback")
    for _ in range(500):
        feedback_type = data["feedback"]["feedback-type"]
        feedback_radio = driver.find_element(By.ID, feedback_type)
        if not feedback_radio.is_selected():
            feedback_radio.click()
        driver.find_element(By.ID, "message").send_keys(data["feedback"]["message"])
        driver.find_element(By.ID, "name").send_keys(data["feedback"]["name"])
        driver.find_element(By.ID, "email").send_keys(data["feedback"]["email"])
        driver.find_element(By.CLASS_NAME, "button").click()
        time.sleep(2)

# Run all form-filling functions
fill_login_form()
# fill_registration_form()
# fill_payment_form()
# fill_feedback_form()

driver.quit()
