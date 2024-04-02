from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pytest
from data import login, password, main_page


# Авторизация
def test_auth_positive(driver):
    driver.get(main_page)

    driver.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    driver.find_element(By.XPATH, '//*[@id="login-button"]').click()
    assert driver.current_url == 'https://www.saucedemo.com/inventory.html', 'url не соответствует ожидаемому'


def test_auth_negative():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element(By.XPATH, '//*[@id="user-name"]').send_keys('user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('user')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()
    browser.implicitly_wait(0.5)
    error_message = browser.find_element(By.XPATH, '//*[@data-test="error"]')
    assert browser.current_url == 'https://www.saucedemo.com/'
    assert error_message.text == 'Epic sadface: Username and password do not match any user in this service'
    browser.quit()


# Корзина
def test_add_product_to_cart_from_catalog():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.XPATH, '//*[@id="add-to-cart-sauce-labs-backpack"]').click()
    assert browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span').text == '1'
    browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a').click()
    assert browser.find_element(By.XPATH, '//*[@class="cart_quantity"]').text == '1'
    browser.quit()

def test_remove_product_from_cart_in_cart():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.XPATH, '//*[@id="add-to-cart-sauce-labs-backpack"]').click()
    assert browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span').text == '1'
    browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a').click()
    assert browser.find_element(By.XPATH, '//*[@class="cart_quantity"]').text == '1'

    browser.find_element(By.XPATH, '//*[@id="remove-sauce-labs-backpack"]').click()
    #assert browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span').is_displayed()
    with pytest.raises(NoSuchElementException):
        browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span')
        pytest.fail('Не должно быть товаров в корзине')
    browser.quit()


def test_add_product_in_cart_from_products_cards():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.XPATH, '//*[@id="item_0_title_link"]').click()
    browser.find_element(By.CSS_SELECTOR, '#add-to-cart').click()
    assert browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span').text == '1'
    browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a').click()
    assert browser.find_element(By.XPATH, '//*[@class="cart_quantity"]').text == '1'
    browser.quit()


def test_remove_product_from_cart_in_products_cards():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.XPATH, '//*[@id="item_0_title_link"]').click()
    browser.find_element(By.CSS_SELECTOR, '#add-to-cart').click()
    assert browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span').text == '1'
    browser.find_element(By.XPATH, '//*[@id="remove"]').click()
    browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a').click()
    with pytest.raises(NoSuchElementException):
        browser.find_element(By.XPATH, '//*[@id="shopping_cart_container"]/a/span')
        pytest.fail('Не должно быть товаров в корзине')
    browser.quit()


# Карточка товара
def test_successful_open_product_card_after_click_om_image_prod():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.XPATH, '//*[@id="item_1_img_link"]').click()
    assert browser.current_url == 'https://www.saucedemo.com/inventory-item.html?id=1'
    browser.quit()

def test_successful_open_product_card_after_click_on_title_prod():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.XPATH, '//*[@id="item_5_title_link"]').click()
    assert browser.current_url == 'https://www.saucedemo.com/inventory-item.html?id=5'
    browser.quit()

# Оформление заказа
def test_placing_an_order_positive():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.XPATH, '//*[@id="add-to-cart-test.allthethings()-t-shirt-(red)"]').click()
    assert browser.find_element(By.CSS_SELECTOR, '.shopping_cart_badge').text == '1'
    browser.find_element(By.CSS_SELECTOR, '.shopping_cart_link').click()
    assert browser.find_element(By.CSS_SELECTOR, '.cart_quantity').text == '1'
    browser.find_element(By.CSS_SELECTOR, '#checkout').click()
    assert browser.current_url == 'https://www.saucedemo.com/checkout-step-one.html'
    browser.find_element(By.CSS_SELECTOR, '#first-name').send_keys('Howard')
    browser.find_element(By.CSS_SELECTOR, '#last-name').send_keys('Lovecraft')
    browser.find_element(By.CSS_SELECTOR, '#postal-code').send_keys('322')
    browser.find_element(By.CSS_SELECTOR, '#continue').click()
    assert browser.current_url == 'https://www.saucedemo.com/checkout-step-two.html'
    browser.find_element(By.CSS_SELECTOR, '#finish').click()
    assert browser.find_element(By.CSS_SELECTOR, '.complete-header').text == 'Thank you for your order!'
    assert browser.find_element(By.CSS_SELECTOR, '.complete-text').text == 'Your order has been dispatched, and will arrive just as fast as the pony can get there!'
    browser.find_element(By.CSS_SELECTOR, '#back-to-products').click()
    assert browser.current_url == 'https://www.saucedemo.com/inventory.html'
    browser.quit()


# Фильтр
def test_checking_filters_from_a_to_z():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.CSS_SELECTOR, '.product_sort_container').click()
    browser.find_element(By.XPATH, '//option[text()="Name (A to Z)"]').click()
    assert len(browser.find_elements(By.CSS_SELECTOR, '.inventory_item')) == 6
    elements = browser.find_elements(By.XPATH, '//*[@class="inventory_item_name "]')
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst)
    browser.quit()


def test_checking_filters_from_z_to_a():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.CSS_SELECTOR, '.product_sort_container').click()
    browser.find_element(By.XPATH, '//option[text()="Name (Z to A)"]').click()
    assert len(browser.find_elements(By.CSS_SELECTOR, '.inventory_item')) == 6
    elements = browser.find_elements(By.XPATH, '//*[@class="inventory_item_name "]')
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, reverse=True)
    browser.quit()


def test_checking_filters_from_low_to_high():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.CSS_SELECTOR, '.product_sort_container').click()
    browser.find_element(By.XPATH, '//option[text()="Price (low to high)"]').click()
    assert len(browser.find_elements(By.CSS_SELECTOR, '.inventory_item')) == 6
    elements = browser.find_elements(By.CSS_SELECTOR, '.inventory_item_price')
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, key=lambda x: float(x[1:]))
    browser.quit()


def test_checking_filters_from_high_to_low():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.CSS_SELECTOR, '.product_sort_container').click()
    browser.find_element(By.XPATH, '//option[text()="Price (high to low)"]').click()
    assert len(browser.find_elements(By.CSS_SELECTOR, '.inventory_item')) == 6
    elements = browser.find_elements(By.CSS_SELECTOR, '.inventory_item_price')
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, key=lambda x: float(x[1:]), reverse=True)
    browser.quit()


# Бургер меню
def test_logout():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.CSS_SELECTOR, '#react-burger-menu-btn').click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.CSS_SELECTOR, '#logout_sidebar_link').click()
    assert browser.current_url == 'https://www.saucedemo.com/'
    browser.quit()


def test_check_button_about():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.CSS_SELECTOR, '#react-burger-menu-btn').click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.CSS_SELECTOR, '#about_sidebar_link').click()
    assert browser.find_element(By.CSS_SELECTOR, 'body').text != '403 Forbidden', 'Страница недоступна: 404'
    browser.quit()


def test_check_button_reset_app_state():
    browser = webdriver.Chrome()
    browser.get('https://www.saucedemo.com/')
    browser.find_element('xpath', '//*[@id="user-name"]').send_keys('standard_user')
    browser.find_element(By.XPATH, '//*[@id="password"]').send_keys('secret_sauce')
    browser.find_element(By.XPATH, '//*[@id="login-button"]').click()

    browser.find_element(By.CSS_SELECTOR, '.product_sort_container').click()
    browser.find_element(By.XPATH, '//option[text()="Name (Z to A)"]').click()
    assert len(browser.find_elements(By.CSS_SELECTOR, '.inventory_item')) == 6
    elements = browser.find_elements(By.XPATH, '//*[@class="inventory_item_name "]')
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst, reverse=True)

    browser.find_element(By.CSS_SELECTOR, '#react-burger-menu-btn').click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.CSS_SELECTOR, '#reset_sidebar_link').click()
    elements = browser.find_elements(By.XPATH, '//*[@class="inventory_item_name "]')
    lst = []
    for e in elements:
        lst.append(e.text)
    assert lst == sorted(lst)

    browser.find_element(By.CSS_SELECTOR, '#add-to-cart-sauce-labs-backpack').click()
    browser.find_element(By.CSS_SELECTOR, '#react-burger-menu-btn').click()
    browser.implicitly_wait(0.5)
    browser.find_element(By.CSS_SELECTOR, '#reset_sidebar_link').click()
    with pytest.raises(NoSuchElementException):
        browser.find_element(By.CSS_SELECTOR, '.shopping_cart_badge')
        pytest.fail('Не должно быть товаров в корзине')
    browser.quit()
