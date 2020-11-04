import os
import logging
import datetime
import argparse

import pandas as pd


class Miscellaneous:
    logger = logging.getLogger('Miscellaneous')

    @staticmethod
    def logger_configure(name='', print_to_console=False):
        os.makedirs('./logs', exist_ok=True)
        logfile = datetime.datetime.today().strftime('%Y-%d-%m')

        handlers = [logging.FileHandler(f'logs/{logfile}.log')]
        if print_to_console:
            handlers.append(logging.StreamHandler())

        logging.basicConfig(
            format='%(asctime)s:%(levelname)s:%(name)s:: %(message)s', datefmt='%H:%M:%S',
            handlers=handlers)
        logging.root.setLevel(logging.INFO)

        return logging.getLogger(name)

    @staticmethod
    def argparser_configure():
        parser = argparse.ArgumentParser()
        parser.add_argument("--stub", help="Skip settings input and take default", action="store_true")
        parser.add_argument("--no-reorder", help="Skip reordering files", action="store_true")
        parser.add_argument("--verbose", help="Enable printing logs to console", action="store_true")
        parser.add_argument("--gmail", help="Set settings for gmail", action="store_true")
        return parser.parse_args()

    @classmethod
    def process_spammed_emails_file(cls, spammed_emails_file: str):
        """ Creates (or reads if exist) excel with list of already spammed mails"""

        if os.path.exists(spammed_emails_file):
            cls.logger.info(f'File {spammed_emails_file} already exists, loading')

            spammed_emails_df = pd.read_excel(spammed_emails_file, usecols=['Email'])
            cls.logger.info(f'{len(spammed_emails_df)} emails found in already spammed excel')

            return spammed_emails_df

        spammed_emails_df = pd.DataFrame(columns=['Email'])
        cls.logger.info(f'File {spammed_emails_file} doesn"t exist, creating blank')

        return spammed_emails_df

    @classmethod
    def remove_intersection(cls, first_df: pd.DataFrame, second_df: pd.DataFrame):
        """ Returns first_df without second_df """

        first_df = first_df[~first_df.isin(second_df)].dropna()
        cls.logger.info(f'{len(first_df)} emails left to spam after removing already spammed')
        return first_df