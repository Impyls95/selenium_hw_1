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
    driver = login

    driver.find_element(By.XPATH, locators.add_backpack).click()
    assert driver.find_element(By.XPATH, locators.cart_badge).text == '1'
    driver.find_element(By.CLASS_NAME, locators.cart_link).click()
    assert driver.find_element(By.CLASS_NAME, locators.cart_quantity).text == '1'


def test_remove_product_from_cart_in_cart(login):
    driver = login

    driver.find_element(By.XPATH, locators.add_backpack).click()
    assert driver.find_element(By.XPATH, locators.cart_badge).text == '1'
    driver.find_element(By.CLASS_NAME, locators.cart_link).click()
    assert driver.find_element(By.CLASS_NAME, locators.cart_quantity).text == '1'

    driver.find_element(By.XPATH, locators.remove_backpack).click()
    #  assert driver.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span').is_displayed()
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.XPATH, locators.cart_badge)
        pytest.fail('Не должно быть товара в корзине')


def test_add_product_in_cart_from_products_cards(login):
    driver = login

    driver.find_element(By.XPATH, locators.item_0_link).click()
    driver.find_element(By.CSS_SELECTOR, locators.add_to_cart).click()
    assert driver.find_element(By.XPATH, locators.cart_badge).text == '1'
    driver.find_element(By.CLASS_NAME, locators.cart_link).click()
    assert driver.find_element(By.CLASS_NAME, locators.cart_quantity).text == '1'


def test_remove_product_from_cart_in_products_cards(login):
    driver = login

    driver.find_element(By.XPATH, locators.item_0_link).click()
    driver.find_element(By.CSS_SELECTOR, locators.add_to_cart).click()
    assert driver.find_element(By.XPATH, locators.cart_badge).text == '1'
    driver.find_element(By.XPATH, locators.remove_from_prod_cart).click()
    driver.find_element(By.CLASS_NAME, locators.cart_link).click()
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.XPATH, locators.cart_badge)
        pytest.fail('Не должно быть товаров в корзине')


# Карточка товара
def test_successful_open_product_card_after_click_om_image_prod(login):
    driver = login

    driver.find_element(By.CSS_SELECTOR, locators.item_1_img_link).click()
    assert driver.current_url == 'https://www.saucedemo.com/inventory-item.html?id=1'


def test_successful_open_product_card_after_click_on_title_prod(login):
    driver = login

    driver.find_element(By.CSS_SELECTOR, locators.item_5_img_link).click()
    assert driver.current_url == 'https://www.saucedemo.com/inventory-item.html?id=5'


# Оформление заказа
def test_placing_an_order_positive(login):
    driver = login

    driver.find_element(By.XPATH, locators.add_to_cart_red_tshirt).click()
    assert driver.find_element(By.XPATH, locators.cart_badge).text == '1'
    driver.find_element(By.CLASS_NAME, locators.cart_link).click()
    assert driver.find_element(By.CLASS_NAME, locators.cart_quantity).text == '1'
    driver.find_element(By.CSS_SELECTOR, locators.checkout).click()
    assert driver.current_url == 'https://www.saucedemo.com/checkout-step-one.html'
    driver.find_element(By.CSS_SELECTOR, locators.first_name_field).send_keys('Howard')
    driver.find_element(By.CSS_SELECTOR, locators.last_name_field).send_keys('Lovecraft')
    driver.find_element(By.CSS_SELECTOR, locators.postal_code).send_keys('322')
    driver.find_element(By.CSS_SELECTOR, locators.continue_btn).click()
    assert driver.current_url == 'https://www.saucedemo.com/checkout-step-two.html'
    driver.find_element(By.CSS_SELECTOR, locators.finish_btn).click()
    assert driver.find_element(By.CSS_SELECTOR, locators.complete_header).text == 'Thank you for your order!'
    assert driver.find_element(By.CSS_SELECTOR, locators.complete_text).text == 'Your order has been dispatched, and will arrive just as fast as the pony can get there!'
    driver.find_element(By.CSS_SELECTOR, locators.back_to_products).click()
    assert driver.current_url == 'https://www.saucedemo.com/inventory.html'


# Фильтр
def test_checking_filters_from_a_to_z(login):
    driver = login

    driver.find_element(By.CSS_SELECTOR, locators.product_sort_container).click()
    driver.find_element(By.XPATH, locators.sort_a_to_z).click()
    assert len(driver.find_elements(By.CSS_SELECTOR, locators.inventory_item)) == 6
    elements = driver.find_elements(By.XPATH, locators.item_names)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst)


def test_checking_filters_from_z_to_a(login):
    driver = login

    driver.find_element(By.CSS_SELECTOR, locators.product_sort_container).click()
    driver.find_element(By.XPATH, locators.sort_z_to_a).click()
    assert len(driver.find_elements(By.CSS_SELECTOR, locators.inventory_item)) == 6
    elements = driver.find_elements(By.XPATH, locators.item_names)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, reverse=True)


def test_checking_filters_from_low_to_high(login):
    driver = login

    driver.find_element(By.CSS_SELECTOR, locators.product_sort_container).click()
    driver.find_element(By.XPATH, locators.sort_low_to_high).click()
    assert len(driver.find_elements(By.CSS_SELECTOR, locators.inventory_item)) == 6
    elements = driver.find_elements(By.CSS_SELECTOR, locators.inventory_item_price)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, key=lambda x: float(x[1:]))


def test_checking_filters_from_high_to_low(login):
    driver = login

    driver.find_element(By.CSS_SELECTOR, locators.product_sort_container).click()
    driver.find_element(By.XPATH, locators.sort_high_to_low).click()
    assert len(driver.find_elements(By.CSS_SELECTOR, locators.inventory_item)) == 6
    elements = driver.find_elements(By.CSS_SELECTOR, locators.inventory_item_price)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, key=lambda x: float(x[1:]), reverse=True)


# Бургер меню
def test_logout(login):
    driver = login

    driver.find_element(By.CSS_SELECTOR, locators.burger_menu_btn).click()
    driver.implicitly_wait(0.5)
    driver.find_element(By.CSS_SELECTOR, locators.logout_link).click()
    assert driver.current_url == 'https://www.saucedemo.com/'


def test_check_button_about(login):
    driver = login

    driver.find_element(By.CSS_SELECTOR, locators.burger_menu_btn).click()
    driver.implicitly_wait(0.5)
    driver.find_element(By.CSS_SELECTOR, locators.about_link).click()
    assert driver.find_element(By.CSS_SELECTOR, locators.body).text != '403 Forbidden', 'Страница недоступна: 404'


def test_check_button_reset_app_state(login):
    driver = login

    driver.find_element(By.CSS_SELECTOR, locators.product_sort_container).click()
    driver.find_element(By.XPATH, locators.sort_z_to_a).click()
    assert len(driver.find_elements(By.CSS_SELECTOR, locators.inventory_item)) == 6
    elements = driver.find_elements(By.XPATH, locators.item_names)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, reverse=True)

    driver.find_element(By.CSS_SELECTOR, locators.burger_menu_btn).click()
    driver.implicitly_wait(0.5)
    driver.find_element(By.CSS_SELECTOR, locators.reset_link).click()
    elements = driver.find_elements(By.XPATH, locators.item_names)
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst)

    driver.find_element(By.CSS_SELECTOR, locators.add_backpack).click()
    driver.find_element(By.CSS_SELECTOR, locators.burger_menu_btn).click()
    driver.implicitly_wait(0.5)
    driver.find_element(By.CSS_SELECTOR, locators.reset_link).click()
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.XPATH, locators.cart_badge)
        pytest.fail('Не должно быть товаров в корзине')
