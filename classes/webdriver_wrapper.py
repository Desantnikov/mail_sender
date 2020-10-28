import logging
from typing import Union
from abc import abstractmethod

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.common.proxy import Proxy

DEFAULT_TIMEOUT, DEFAULT_LOCATOR_TYPE = 5, 'xpath'


class WebdriverWrapper:
    # TODO: Try to create one action chain for all

    def __init__(self, config: dict = None, path_to_driver: str = None, logger: logging.Logger = None, proxy: Proxy = None):

        self.logger = logger or logging.getLogger('WebdriverWrapper')

        # print('setting proxy')
        # self.profile = webdriver.FirefoxProfile()
        # self.profile.set_preference("network.proxy.type", 1)
        # self.profile.set_preference("network.proxy.socks", "91.203.36.102")
        # self.profile.set_preference("network.proxy.socks_port", 48641)
        # self.profile.set_preference("network.proxy.socks_version", 4)
        # self.profile.update_preferences()

        self.driver = webdriver.Chrome()#firefox_profile=self.profile)

        self.config = config

    @abstractmethod
    def log_in(self):
        pass

    def load_page(self, url: str):
        self.driver.get(url)

    def wait_and_click(self, locator_value: str = None, locator_type: str = DEFAULT_LOCATOR_TYPE,
                       click_type: str = 'once', timeout: int = DEFAULT_TIMEOUT):

        element = self.wait(locator_value=locator_value, locator_type=locator_type, timeout=timeout)

        if click_type == 'once':
            element.click()
        elif click_type == 'double':
            ActionChains(self.driver).double_click(element).perform()
        elif click_type == 'shift+click':
            ActionChains(self.driver).key_down(Keys.SHIFT).click(element).key_up(Keys.SHIFT).perform()

    def wait_and_send_keys(self, locator_value: str = None, locator_type: str = DEFAULT_LOCATOR_TYPE, keys: str = None,
                           clear: bool = True, timeout: int = DEFAULT_TIMEOUT):
        element = self.wait(locator_value=locator_value, locator_type=locator_type, timeout=timeout)
        if clear:
            element.clear()

        element.send_keys(keys)

    def wait_and_send_combination(self, locator_value: str = None, locator_type: str = DEFAULT_LOCATOR_TYPE,
                                  combination: str = None, timeout: int = DEFAULT_TIMEOUT):
        element = self.wait(locator_value=locator_value, locator_type=locator_type, timeout=timeout)
        self.send_combination(element=element, combination=combination)

    def wait(self, locator_value: str = None, locator_type: str = DEFAULT_LOCATOR_TYPE, timeout: int = DEFAULT_TIMEOUT):
        """ returns element if it is clickable within <timeout> seconds or raises an exception """

        self.logger.info(f'Waiting for locator "{locator_value}" of type "{locator_type}"; timeout: {timeout}')

        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((locator_type, locator_value)))

        self.logger.info(
            f'Tag "{element.tag_name}" with text "{element.text.encode("unicode-escape")}" became clickable')

        return element

    def send_combination(self, element: FirefoxWebElement = None, combination: str = None):
        # TODO: send directly instead of using currently focused element
        if combination == 'ctrl+v':
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('V').key_up(Keys.CONTROL).perform()
        if combination == 'enter':
            ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()

    # def find_iframes(self):
    #     return self.driver.find_elements_by_tag_name("iframe")

    def switch_to_iframe(self, iframe: Union[WebElement, str]):
        print(f'Switching to {iframe}')

        if iframe == 'parent':
            self.driver.switch_to.parent_frame()
            return

        self.driver.switch_to.frame(iframe)