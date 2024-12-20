import time
from selenium import webdriver
from selenium.webdriver.common.by import By

#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')

url = 'https://parsinger.ru/selenium/1/1.html'

profile_params = ['MAX', 'PETROV', 'divma', '12', 'samara', 'per@pr.ru']
with webdriver.Chrome() as browser:
    browser.get(url)
    input_form = browser.find_elements(By.CLASS_NAME, 'form')
    for i, el in enumerate(input_form):
        el.send_keys(profile_params[i])
    browser.find_element(By.ID, 'btn').click()
    print(browser.find_element(By.ID, 'result').text)
