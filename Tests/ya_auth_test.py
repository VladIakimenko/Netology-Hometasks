import atexit
import sys

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config import LOGIN, PASSWORD

URL = 'https://passport.yandex.ru/auth/list'
ERROR_LOG = 'errors.txt'


class Selenium:
    def __init__(self):
        self.url = URL
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        atexit.register(self.terminate)

    def get(self, url):
        self.driver.get(url)

    def terminate(self):
        if self.driver:
            self.driver.quit()


def test_auth_form(selenium):
    """
    The test assumes that the account is not set up to sms-authentication!
    """
    with open(ERROR_LOG, 'wt', encoding='UTF-8') as error_log:
        sys.stderr = error_log
        selenium.get(URL)

        login_field = WebDriverWait(selenium.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="passp-field-login"]'))
        )
        login_field.send_keys(LOGIN)

        button = selenium.driver.find_element(By.XPATH, '//*[@id="passp:sign-in"]')
        button.click()

        pass_field = WebDriverWait(selenium.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="passp-field-passwd"]'))
        )
        pass_field.send_keys(PASSWORD)

        submit = selenium.driver.find_element(By.XPATH, '//*[@id="passp:sign-in"]')
        submit.click()

        WebDriverWait(selenium.driver, 20).until(
            EC.url_to_be('https://id.yandex.ru/')
        )
        assert 'id.yandex.ru' in selenium.driver.current_url


if __name__ == '__main__':
    driver = Selenium()
    test_auth_form(driver)
