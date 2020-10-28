from classes.webdriver_wrapper import WebdriverWrapper


class UkrNetWrapper(WebdriverWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log_in(self):
        self.load_page('https://mail.ukr.net/')

        # enter login
        self.wait_and_send_keys(locator_value='//*[@id="id-l"]', keys=self.config['login'])

        # enter password
        self.wait_and_send_keys(locator_value='//*[@id="id-p"]', keys=self.config['password'])

        # click "enter"
        self.wait_and_click(locator_value='/html/body/div/div/main/form/button')
