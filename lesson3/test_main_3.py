import time
import pytest
from data_3 import site_victor, login_victor, pass_victor
from locators_3 import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement


def test_one(driver, wait):   # С использованием Explicit waits и Expected Conditions
    driver.get(site_victor)
    assert driver.find_element(*zagolovok).text == 'Практика с ожиданиями в Selenium'

    start_testing = wait.until(EC.element_to_be_clickable(button_start_testing))
    assert start_testing.text == 'Начать тестирование'

    start_testing.click()
    driver.find_element(*input_login).send_keys(login_victor)
    driver.find_element(*input_pass).send_keys(pass_victor)
    driver.find_element(*checkbox_agree).click()
    driver.find_element(*button_reg).click()

    loading = driver.find_element(*loader)
    assert loading.is_displayed()
    wait.until(EC.invisibility_of_element(loader))
    assert driver.find_element(*successful_text).is_displayed()


def test_two(driver_impl):     # С использованием Implicit waits
    driver_impl.get(site_victor)
    assert driver_impl.find_element(*zagolovok).text == 'Практика с ожиданиями в Selenium'
    time.sleep(5)
    assert driver_impl.find_element(*button_start_testing).text == 'Начать тестирование'

    driver_impl.find_element(*button_start_testing).click()
    driver_impl.find_element(*input_login).send_keys(login_victor)
    driver_impl.find_element(*input_pass).send_keys(pass_victor)
    driver_impl.find_element(*checkbox_agree).click()
    driver_impl.find_element(*button_reg).click()
    loading = driver_impl.find_element(*loader)
    assert loading.is_displayed()

    time.sleep(5)
    assert driver_impl.find_element(*successful_text).is_displayed()


def test_three(driver):     # С использованием time.sleep()
    driver.get(site_victor)
    assert driver.find_element(*zagolovok).text == 'Практика с ожиданиями в Selenium'

    time.sleep(5)
    assert driver.find_element(*button_start_testing).text == 'Начать тестирование'

    driver.find_element(*button_start_testing).click()
    driver.find_element(*input_login).send_keys(login_victor)
    driver.find_element(*input_pass).send_keys(pass_victor)
    driver.find_element(*checkbox_agree).click()
    driver.find_element(*button_reg).click()
    loading = driver.find_element(*loader)
    assert loading.is_displayed()

    time.sleep(5)
    assert driver.find_element(*successful_text).is_displayed()
