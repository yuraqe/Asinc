from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By



chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

url = 'https://parsinger.ru/selenium/5.5/5/1.html'

with webdriver.Chrome(options=chrome_options) as browser:
    browser.get(url)
    elems = browser.find_elements(By.CSS_SELECTOR,'div[style]')[1:]
    for elem in elems:
        color_hex = elem.find_element(By.CSS_SELECTOR, 'span').text
        res_btn = elem.find_elements(By.CSS_SELECTOR, 'option[value]')
        for res in res_btn:
            if res.text.strip() == color_hex.strip():
                res.click()
        button_color = elem.find_elements(By.CSS_SELECTOR, 'button[data-hex]')
        for btn in button_color:
            if btn.get_attribute('data-hex').strip() == color_hex:
                btn.click()
        elem.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]').click()
        elem.find_element(By.CSS_SELECTOR, 'input[type="text"]').send_keys(color_hex)
        elem.find_element(By.XPATH, "//button[text()='Проверить']").click()


    button = browser.find_element(By.XPATH, "//button[text()='Проверить все элементы']")
    button.click()
    sleep(2)
    alert = browser.switch_to.alert
    alert_text = alert.text
    print(alert_text)
