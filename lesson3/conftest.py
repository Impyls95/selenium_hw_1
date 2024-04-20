from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def chrome_options():
    options = Options()
    options.add_argument('--incognito')
    return options


@pytest.fixture
def driver(chrome_options):
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


@pytest.fixture
def wait(driver):
    wait = WebDriverWait(driver, timeout=10)
    return wait


@pytest.fixture
def driver_impl(chrome_options):
    driver_impl = webdriver.Chrome(options=chrome_options)
    driver_impl.implicitly_wait(10)
    yield driver_impl
    driver_impl.quit()
