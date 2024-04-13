import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from data import user_login, password, main_page
import locators


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    yield driver
    print('\nquit browser...')
    driver.quit()


@pytest.fixture()
def login(driver):
    driver.get(main_page)
    driver.find_element(By.XPATH, locators.username_field).send_keys(user_login)
    driver.find_element(By.XPATH, locators.password_field).send_keys(password)
    driver.find_element(By.XPATH, locators.login_button).click()
    yield driver
    driver.quit()
