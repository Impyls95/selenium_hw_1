from selenium.webdriver.common.by import By


# https://victoretc.github.io/selenium_waits/
zagolovok = (By.XPATH, '/html/body/h1')
button_start_testing = (By.XPATH, '//button[text()="Начать тестирование"]')
input_login = (By.CSS_SELECTOR, '#login')
input_pass = (By.CSS_SELECTOR, '#password')
checkbox_agree = (By.CSS_SELECTOR, '#agree')
button_reg = (By.CSS_SELECTOR, '#register')
loader = (By.CSS_SELECTOR, '#loader')
successful_text = (By.XPATH, '//p[text()="Вы успешно зарегистрированы!"]')

# heroku
button_add_elem = (By.XPATH, '//button[text()="Add Element"]')
button_delete = (By.XPATH, '//button[text()="Delete"]')
successful_auth_heroku = (By.XPATH, '//*[@id="content"]/div/p')
broken_image_locator = (By.XPATH, '//*[@id="content"]/div/img')
