import time

import autoit

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

    def send_mail(self, mail):
        # click "write email"
        self.wait_and_click(locator_value='//*[@id="content"]/aside/button')

        # fill recipient input
        self.wait_and_send_keys(locator_value='//*[@id="screens"]/div/div[2]/section[1]/div[1]/div[4]/input[2]',
                                keys=mail.recipient)

        # fill topic input
        self.wait_and_send_keys(locator_value='//*[@id="screens"]/div/div[2]/section[1]/div[4]/div[2]/input',
                                keys=mail.topic)

        # switch to iframe with mail body input
        self.switch_to_iframe(iframe=self.driver.find_element_by_xpath('//*[@id="mce_0_ifr"]'))

        # fill mail body input
        self.wait_and_send_keys('//*[@id="tinymce"]', keys=str(mail))  # TODO: !!!!

        # return to parent iframe
        self.switch_to_iframe(iframe='parent')

        # attach files one by one
        file_dialogue_window_title = "[CLASS:#32770; TITLE:Open]"
        default_windows_timeout = 15

        for file in mail.attachment_files_sequence:
            # click attach file button
            self.wait_and_click(locator_value='//*[@id="screens"]/div/div[2]/section[2]/div[2]/label/button')

            # wait until file selector dialogue window will open
            autoit.win_wait(file_dialogue_window_title, default_windows_timeout)
            time.sleep(1)

            # fill input with file path
            autoit.control_set_text(file_dialogue_window_title, "Edit1", file)
            time.sleep(1)

            # click "OK"
            autoit.control_click(file_dialogue_window_title, "Button1")
            time.sleep(1)

        # check if amount of attached attachments == attachments
        attachment_list_children = self.driver.find_elements_by_css_selector('#screens > div > div.screen__content > '
                                                                             'section.sendmsg__attachments > div.'
                                                                             'sendmsg__attachments-list > div')
        if not len(attachment_list_children) == len(mail.attachment_files_sequence):
            print('Error!')

        print('going to send!')
        time.sleep(10)
        # click on "send" button
        self.wait_and_click(locator_value='//*[@id="screens"]/div/div[1]/div/button')
