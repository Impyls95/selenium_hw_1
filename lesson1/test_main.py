from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pytest
from data import user_login, password, main_page, wrong_login_and_pass
import locators


# Авторизация
def test_auth_positive(driver):
    driver.get(main_page)

    driver.find_element(By.XPATH, locators.username_field).send_keys(user_login)
    driver.find_element(By.XPATH, locators.password_field).send_keys(password)
    driver.find_element(By.XPATH, locators.login_button).click()
    assert driver.current_url == 'https://www.saucedemo.com/inventory.html', 'url не соответствует ожидаемому'


def test_auth_negative(driver):
    driver.get(main_page)

    driver.find_element(By.XPATH, locators.username_field).send_keys(wrong_login_and_pass)
    driver.find_element(By.XPATH, locators.password_field).send_keys(wrong_login_and_pass)
    driver.find_element(By.XPATH, locators.login_button).click()
    driver.implicitly_wait(0.5)
    error_message = driver.find_element(By.XPATH, locators.error_locator)
    assert driver.current_url == 'https://www.saucedemo.com/'
    assert error_message.text == 'Epic sadface: Username and password do not match any user in this service'


# Корзина
def test_add_product_to_cart_from_catalog(login):
    browser = login

    browser.find_element(By.XPATH, locators.add_backpack).click()
    assert browser.find_element(By.XPATH, locators.cart_badge).text == '1'
    browser.find_element(By.CLASS_NAME, locators.cart_link).click()
    assert browser.find_element(By.CLASS_NAME, locators.cart_quantity).text == '1'


def test_remove_product_from_cart_in_cart(login):
    browser = login

    browser.find_element(By.XPATH, locators.add_backpack).click()
    assert browser.find_element(By.XPATH, locators.cart_badge).text == '1'
    browser.find_element(By.CLASS_NAME, locators.cart_link).click()
    assert browser.find_element(By.CLASS_NAME, locators.cart_quantity).text == '1'

    browser.find_element(By.XPATH, locators.remove_backpack).click()
    #  assert browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span').is_displayed()
    with pytest.raises(NoSuchElementException):
        browser.find_element(By.XPATH, locators.cart_badge)
        pytest.fail('Не должно быть товара в корзине')


def test_add_product_in_cart_from_products_cards(login):
    browser = login

    browser.find_element(By.XPATH, locators.item_0_link).click()
    browser.find_element(By.CSS_SELECTOR, locators.add_to_cart).click()
    assert browser.find_element(By.XPATH, locators.cart_badge).text == '1'
    browser.find_element(By.CLASS_NAME, locators.cart_link).click()
    assert browser.find_element(By.CLASS_NAME, locators.cart_quantity).text == '1'


def test_remove_product_from_cart_in_products_cards(login):
    browser = login

    browser.find_element(By.XPATH, locators.item_0_link).click()
    browser.find_element(By.CSS_SELECTOR, locators.add_to_cart).click()
    assert browser.find_element(By.XPATH, locators.cart_badge).text == '1'
    browser.find_element(By.XPATH, locators.remove_from_prod_cart).click()
    browser.find_element(By.CLASS_NAME, locators.cart_link).click()
    with pytest.raises(NoSuchElementException):
        browser.find_element(By.XPATH, locators.cart_badge)
        pytest.fail('Не должно быть товаров в корзине')


# Карточка товара
def test_successful_open_product_card_after_click_om_image_prod(login):
    browser = login

    browser.find_element(By.CSS_SELECTOR, locators.item_1_img_link).click()
    assert browser.current_url == 'https://www.saucedemo.com/inventory-item.html?id=1'


def test_successful_open_product_card_after_click_on_title_prod(login):
    browser = login

    browser.find_element(By.CSS_SELECTOR, locators.item_5_img_link).click()
    assert browser.current_url == 'https://www.saucedemo.com/inventory-item.html?id=5'


# Оформление заказа
def test_placing_an_order_positive(login):
    browser = login

    browser.find_element(By.XPATH, locators.add_to_cart_red_tshirt).click()
    assert browser.find_element(By.XPATH, locators.cart_badge).text == '1'
    browser.find_element(By.CLASS_NAME, locators.cart_link).click()
    assert browser.find_element(By.CLASS_NAME, locators.cart_quantity).text == '1'
    browser.find_element(By.CSS_SELECTOR, locators.checkout).click()
    assert browser.current_url == 'https://www.saucedemo.com/checkout-step-one.html'
    browser.find_element(By.CSS_SELECTOR, locators.first_name_field).send_keys('Howard')
    browser.find_element(By.CSS_SELECTOR, locators.last_name_field).send_keys('Lovecraft')
    browser.find_element(By.CSS_SELECTOR, locators.postal_code).send_keys('322')
    browser.find_element(By.CSS_SELECTOR, locators.continue_btn).click()
    assert browser.current_url == 'https://www.saucedemo.com/checkout-step-two.html'
    browser.find_element(By.CSS_SELECTOR, locators.finish_btn).click()
    assert browser.find_element(By.CSS_SELECTOR, locators.complete_header).text == 'Thank you for your order!'
    assert (browser.find_element(By.CSS_SELECTOR, locators.complete_text).text ==
            'Your order has been dispatched, and will arrive just as fast as the pony can get there!')
    browser.find_element(By.CSS_SELECTOR, locators.back_to_products).click()
    assert browser.current_url == 'https://www.saucedemo.com/inventory.html'


# Фильтр
def test_checking_filters_from_a_to_z(login):
    browser = login

    browser.find_element(By.CSS_SELECTOR, locators.product_sort_container).click()
    browser.find_element(By.XPATH, locators.sort_a_to_z).click()
    assert len(browser.find_elements(By.CSS_SELECTOR, locators.inventory_item)) == 6
    elements = browser.find_elements(By.XPATH, locators.item_names)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst)


def test_checking_filters_from_z_to_a(login):
    browser = login

    browser.find_element(By.CSS_SELECTOR, locators.product_sort_container).click()
    browser.find_element(By.XPATH, locators.sort_z_to_a).click()
    assert len(browser.find_elements(By.CSS_SELECTOR, locators.inventory_item)) == 6
    elements = browser.find_elements(By.XPATH, locators.item_names)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, reverse=True)


def test_checking_filters_from_low_to_high(login):
    browser = login

    browser.find_element(By.CSS_SELECTOR, locators.product_sort_container).click()
    browser.find_element(By.XPATH, locators.sort_low_to_high).click()
    assert len(browser.find_elements(By.CSS_SELECTOR, locators.inventory_item)) == 6
    elements = browser.find_elements(By.CSS_SELECTOR, locators.inventory_item_price)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, key=lambda x: float(x[1:]))


def test_checking_filters_from_high_to_low(login):
    browser = login

    browser.find_element(By.CSS_SELECTOR, locators.product_sort_container).click()
    browser.find_element(By.XPATH, locators.sort_high_to_low).click()
    assert len(browser.find_elements(By.CSS_SELECTOR, locators.inventory_item)) == 6
    elements = browser.find_elements(By.CSS_SELECTOR, locators.inventory_item_price)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, key=lambda x: float(x[1:]), reverse=True)


# Бургер меню
def test_logout(login):
    browser = login

    browser.find_element(By.CSS_SELECTOR, locators.burger_menu_btn).click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.CSS_SELECTOR, locators.logout_link).click()
    assert browser.current_url == 'https://www.saucedemo.com/'


def test_check_button_about(login):
    browser = login

    browser.find_element(By.CSS_SELECTOR, locators.burger_menu_btn).click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.CSS_SELECTOR, locators.about_link).click()
    assert browser.find_element(By.CSS_SELECTOR, locators.body).text != '403 Forbidden', 'Страница недоступна: 404'


def test_check_button_reset_app_state(login):
    browser = login

    browser.find_element(By.CSS_SELECTOR, locators.product_sort_container).click()
    browser.find_element(By.XPATH, locators.sort_z_to_a).click()
    assert len(browser.find_elements(By.CSS_SELECTOR, locators.inventory_item)) == 6
    elements = browser.find_elements(By.XPATH, locators.item_names)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, reverse=True)

    browser.find_element(By.CSS_SELECTOR, locators.burger_menu_btn).click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.CSS_SELECTOR, locators.reset_link).click()
    elements = browser.find_elements(By.XPATH, locators.item_names)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst)

    browser.find_element(By.CSS_SELECTOR, locators.add_backpack).click()
    browser.find_element(By.CSS_SELECTOR, locators.burger_menu_btn).click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.CSS_SELECTOR, locators.reset_link).click()
    with pytest.raises(NoSuchElementException):
        browser.find_element(By.XPATH, locators.cart_badge)
        pytest.fail('Не должно быть товаров в корзине')


# Чек бокс
def test_check_box():
    browser = webdriver.Chrome()
    browser.get('https://victoretc.github.io/webelements_information/')
    browser.find_element(By.CSS_SELECTOR, locators.check_login).send_keys('1')
    browser.find_element(By.CSS_SELECTOR, locators.check_password).send_keys('1')

    assert browser.find_element(By.CSS_SELECTOR, locators.check_reg_button).get_attribute('disabled')
