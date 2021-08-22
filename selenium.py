import re
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class Selenium:
    def __init__(self, url: str, timeout=60, page_timeout=5, headless=True):
        self.timeout = timeout
        self.driver: WebDriver = None
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")

        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options
        )
        self.driver.set_page_load_timeout(page_timeout)

        try:
            self.driver.get(url)
        except Exception as e:
            print(e)

    def __enter__(self):
        return self

    def __exit__(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_text_by_xpath(self, xpath: str) -> str:
        """
        Args:
            xpath (str): html xpath

        Returns:
            str: html tag text
        """

        tag_text = None
        try:
            self.driver.implicitly_wait(self.timeout)
            tag_text = self.driver.find_element_by_xpath(xpath).text
        except Exception as e:
            print(e)
        return tag_text

    def click_by_xpath(self, xpath: str):
        """
        Args:
            xpath(str): html xpath

        Returns:
            void
        """

        try:
            self.driver.implicitly_wait(self.timeout)
            self.driver.find_element_by_xpath(xpath).click()
        except Exception as e:
            print(e)

    def go_to(self, url: str):
        """
        Args:
            url(str): 홈페이지 주소

        Returns:
            void: 없음
        """

        try:
            self.driver.execute_script("location.href='{}'".format(url))
        except Exception as e:
            print(e)

    def back(self):
        """
        Returns:
            void: 없음

        """

        try:
            self.driver.back()
        except Exception as e:
            print(e)

    def get_attribute_by_xpath(self, xpath: str, attribute_name: str) -> str:
        """
        Args:
            xpath(str): html xpath
            attribute_name(str): html 속성명

        Returns:
            str: html tag text
        """

        tag_attribute = None
        try:
            self.driver.implicitly_wait(self.timeout)
            tag_attribute = self.driver.find_element_by_xpath(xpath).get_attribute(
                attribute_name
            )
        except Exception as e:
            print(e)
        return tag_attribute
