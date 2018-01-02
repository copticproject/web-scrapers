from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from lib.settings import Settings


class WebTests:
    __driver = None

    def __init__(self):
        self.__driver = webdriver.Remote(command_executor=Settings.getSeleniumRemote(),
            desired_capabilities=DesiredCapabilities.CHROME)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__driver.quit()

    def go_to(self, url):
        self.__driver.get(url)

    def find(self, xpath):
        try:
            return self.__driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return None

    def find_all(self, xpath):
        return self.__driver.find_elements_by_xpath(xpath)

    def css_find(self, css_selector):
        try:
            return self.__driver.find_element_by_css_selector(css_selector)
        except NoSuchElementException:
            return None

    def css_find_all(self, css_selector):
        return self.__driver.find_elements_by_css_selector(css_selector)

    def css_wait(self, css_selector, text, timeout=60):
        WebDriverWait(self.__driver, timeout).until(
            expected_conditions.text_to_be_present_in_element(
                (By.CSS_SELECTOR,css_selector),text))

    def css_wait_not(self, css_selector, text, timeout=60):
        WebDriverWait(self.__driver, timeout).until_not(
            expected_conditions.text_to_be_present_in_element(
                (By.CSS_SELECTOR,css_selector),text))

    def click(self, element):
        self.__driver.execute_script("arguments[0].click();", element)