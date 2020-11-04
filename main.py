from smtplib import SMTPAuthenticationError

from classes.miscellaneous import Miscellaneous
from classes.config import Config
from classes.email_files_sequence import EmailFilesSequence
from classes.mail import Mail


if __name__ == '__main__':
    args = Miscellaneous.argparser_configure()
    logger = Miscellaneous.logger_configure(name='Main', print_to_console=args.verbose)

    config = Config(args=args)
    logger.info(f'Got input values:\r\n{config}')

    mail_template = Mail(**config.get_mail_settings())

    spammed_emails_df = Miscellaneous.process_spammed_emails_file(spammed_emails_file=config.spammed_emails_file)
    emails_to_spam_df = EmailFilesSequence(folder=config.folder_with_excels, reorder=not args.no_reorder).emails_df

    emails_to_spam_df = Miscellaneous.remove_intersection(emails_to_spam_df, spammed_emails_df)

    for counter, email in enumerate(emails_to_spam_df.Email.values, start=1):
        try:
            mail_template.send_to(receiver_email=email)
            spammed_emails_df = spammed_emails_df.append({'Email': email}, ignore_index=True)

        except SMTPAuthenticationError as e:
            logger.exception(f'Failed to authenticate', exc_info=e)
            break

        except Exception as e:
            logger.exception(f'Unexpected exception happened during spamming', exc_info=e)
            continue

        finally:
            spammed_emails_df.to_excel(config.spammed_emails_file)