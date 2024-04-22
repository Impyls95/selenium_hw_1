import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from data_3 import site_heroku
from locators_3 import *


def test_one_create_and_del_elem(driver):   # Необходимо создать и удалить элемент
    driver.get(site_heroku + 'add_remove_elements/')
    assert driver.find_element(*button_add_elem).text == 'Add Element'

    driver.find_element(*button_add_elem).click()
    assert driver.find_element(*button_delete).is_displayed()

    driver.find_element(*button_delete).click()
    assert len(driver.find_elements(*button_delete)) == 0


def test_basic_auth(driver, wait):    # Необходимо пройти базовую авторизацию
    # driver.get(site_heroku + 'basic_auth')
    # # wait.until(EC.alert_is_present())
    # # alert = driver.switch_to.alert
    # # alert.send_keys('admin')
    # # alert.send_keys(Keys.TAB)
    # # alert.send_keys('admin')
    # # alert.accept()
    driver.get('http://admin:admin@the-internet.herokuapp.com/basic_auth')

    assert driver.find_element(*successful_auth_heroku).text == 'Congratulations! You must have the proper credentials.'


def test_find_broken_image(driver):  # Необходимо найти сломанные изображения
    driver.get(site_heroku + 'broken_images')
    images = driver.find_elements(*image_locator)
    broken_src_out = []
    for img in images:
        image_url = img.get_attribute('src')
        response = requests.head(image_url)
        if response.status_code != 200:
            broken_src_out.append(image_url)
    print('Ссылки на сломанные изображения:', broken_src_out)


def test_checkbox_practice(driver):  # Практика с чек боксами
    driver.get(site_heroku + 'checkboxes')
    checkbox_1 = driver.find_element(*btn_checkbox_1)
    checkbox_2 = driver.find_element(*btn_checkbox_2)
    assert not checkbox_1.get_attribute('checked')
    assert checkbox_2.is_selected()

    checkbox_1.click()
    checkbox_2.click()
    assert checkbox_1.is_selected()
    assert not checkbox_2.get_attribute('checked')

