import pytest
from locators_3 import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_add_box(driver, wait):
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    driver.find_element(*add_box).click()
    box_0 = wait.until(EC.visibility_of_element_located(box_0_locator))
    assert box_0.is_displayed()
    driver.find_element(*add_box).click()
    box_1 = wait.until(EC.visibility_of_element_located(box_1_locator))
    assert box_1.is_displayed()


def test_reveal_a_new_input(driver, wait):
    driver.get('https://www.selenium.dev/selenium/web/dynamic.html')
    assert not driver.find_element(*revealed_inp).is_displayed()
    driver.find_element(*btn_reveal_input).click()
    new_input = wait.until(EC.visibility_of_element_located(revealed_inp))
    assert new_input.is_displayed()


def test_demo_qa_1(driver, wait):
    driver.get('https://demoqa.com/dynamic-properties')
    btn_enable_after = wait.until(EC.element_to_be_clickable(enable_after))
    assert btn_enable_after.is_enabled()


def test_demo_qa_2(driver, wait):
    driver.get('https://demoqa.com/dynamic-properties')
    btn_visible_after_5_sec = wait.until(EC.element_to_be_clickable(visible_after))
    assert btn_visible_after_5_sec.text == 'Visible After 5 Seconds'


def test_dynamic_loading_1(driver, wait):
    driver.get('https://the-internet.herokuapp.com/dynamic_loading/1')
    driver.find_element(*start_dyn_load).click()
    load_elem = wait.until(EC.visibility_of_element_located(finish_locator))
    assert load_elem.is_displayed()


def test_dynamic_loading_2(driver, wait):
    driver.get('https://the-internet.herokuapp.com/dynamic_loading/2')
    driver.find_element(*start_dyn_load).click()
