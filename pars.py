import time
from sys import excepthook
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')

url = 'https://parsinger.ru/selenium/5.7/4/index.html'
total = 0
#options=chrome_options
with webdriver.Chrome() as browser:
    browser.get(url)
    child_cont = browser.find_element(By.CSS_SELECTOR, 'div.child_container')
    for _ in range(110):
        try:
            ActionChains(browser).scroll_to_element(child_cont).perform()
            values = child_cont.find_elements(By.CSS_SELECTOR, 'input[type=checkbox]')
            for value in values:
                value_digit = value.get_attribute('value')
                if int(value_digit) % 2 == 0:
                    value.click()
            child_cont = child_cont.find_element(By.XPATH, 'following-sibling::div[@class="child_container"]')
        except:
            break

    time.sleep(3)
    browser.find_element(By.CLASS_NAME, 'alert_button').click()
    time.sleep(2)
    alert = browser.switch_to.alert
    print(alert.text)

