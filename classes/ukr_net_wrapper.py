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

        # fill mail body input
        self._fill_body_with_formatting(mail.body)

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

    def _switch_to_mail_body_iframe(self):
        self.switch_to_iframe(iframe=self.driver.find_element_by_xpath('//*[@id="mce_0_ifr"]'))

    def _set_text_align(self, align):
        print(f'Align changes and now: {align}')

        if not align:
            return

        # open aligns dropdown
        self.wait_and_click(locator_value='//*[@id="mceu_11"]/button[1]/div')

        aligns_dict = {'LEFT': '//*[@id="mceu_35"]/ul/li[1]',
                       'RIGHT': '//*[@id="mceu_35"]/ul/li[3]',
                       'CENTER': '//*[@id="mceu_35"]/ul/li[2]'}


        # click on align's button
        self.wait_and_click(locator_value=aligns_dict[align])

    def _fill_body_with_formatting(self, body):
        for text_part in body:
            # aligns dropdown is placed outside of mail's body iframe
            self.switch_to_iframe(iframe='parent')

            # set align of just written text
            self._set_text_align(text_part.alignment)

            # return to body iframe
            self._switch_to_mail_body_iframe()

            # blank paragraph = newline
            if text_part.text == '':
                self.wait_and_send_combination(locator_value='//*[@id="tinymce"]', combination='enter')
            else:
                # fill body textbox
                self.wait_and_send_keys('//*[@id="tinymce"]', keys=text_part.text, clear=False)

            # start new paragraph
            self.wait_and_send_combination(locator_value='//*[@id="tinymce"]', combination='enter')

        print('filled!!!!')
