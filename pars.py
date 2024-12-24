import time
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

with webdriver.Chrome() as driver:
    driver.get("https://parsinger.ru/selenium/5.10/6/index.html")
#    driver.maximize_window()
    sleep(1)
    actions = ActionChains(driver)
    sliders = driver.find_elements(By.CSS_SELECTOR, '.slider-container')
    for slider in sliders:
        slider_range = slider.find_element(By.CSS_SELECTOR, '.volume-slider')
        width = slider_range.size['width']
        offset = width // 100
        target = slider.find_element(By.CSS_SELECTOR, '.target-value').text
        difference = abs(50 - int(target))
        if int(target) > 50:
            actions.click_and_hold(slider_range).perform()
            for i in range(difference):
                slider_range.send_keys(Keys.ARROW_RIGHT)
            actions.release(slider_range).perform()
        else:
            actions.click_and_hold(slider_range).perform()
            for i in range(difference):
                slider_range.send_keys(Keys.ARROW_LEFT)
            actions.release(slider_range).perform()



    time.sleep(1)
    print(driver.find_element(By.ID, 'message').text)
