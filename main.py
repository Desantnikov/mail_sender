import datetime
import logging
import os
import sys

import pandas as pd

from classes.config import Config
from classes.email_files_sequence import EmailFilesSequence
from classes.mail import Mail

STUB = False


def logger_configure():
    os.makedirs('./logs', exist_ok=True)
    logfile = datetime.datetime.today().strftime('%Y-%d-%m')
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(name)s:: %(message)s', datefmt='%H:%M:%S',
        handlers=[logging.FileHandler(f'logs/{logfile}.log'), logging.StreamHandler()])
    logging.root.setLevel(logging.INFO)


if __name__ == '__main__':
    logger_configure()
    logger = logging.getLogger('Main')
    logger.addHandler(logging.StreamHandler(sys.stdout))

    config = Config(stub=STUB)
    logger.info(f'Got input values:\r\n{config}')

    mail_template = Mail(smtp_url=config.smtp_url, smtp_port=config.smtp_port, sender_email=config.sender_email,
                         sender_password=config.sender_password, body=config.body, subject=config.subject,
                         files_to_attach_sequence=config.files_to_attach_sequence)

    emails_to_spam_df = EmailFilesSequence(folder=config.folder_with_excels, files_template='*.xls*',
                                           reorder_on_creation=not STUB).emails_df

    if os.path.exists(config.spammed_emails_file):
        logger.info(f'File {config.spammed_emails_file} already exists, loading')

        spammed_emails_df = pd.read_excel(config.spammed_emails_file, usecols=['Email'])
        logger.info(f'{len(spammed_emails_df)} emails found in already spammed excel')

        # exclude intersection
        emails_to_spam_df = emails_to_spam_df[~emails_to_spam_df.isin(spammed_emails_df)].dropna()
        logger.info(f'{len(emails_to_spam_df)} emails left to spam after removing already spammed')

    else:
        spammed_emails_df = pd.DataFrame(columns=['Email'])
        logger.info(f'File {config.spammed_emails_file} doesn"t exist, creating blank')

    for counter, email in enumerate(emails_to_spam_df.Email.values, start=1):
        try:
            # every 50th mail
            if not(counter % 50):
                logger.info(f'Sending {counter}th mail; {len(emails_to_spam_df.Email.values)-counter} left')

            mail_template.send_to(receiver_email=email)
            spammed_emails_df = spammed_emails_df.append({'Email': email}, ignore_index=True)

        except Exception as e:
            logger.exception(f'Exception happened during spamming')
            continue
