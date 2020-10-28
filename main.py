import docx
import pandas as pd

from classes.file_classes import FilesSequence
from classes.mail_classes import MailTemplate, Mail
from classes.ukr_net_wrapper import UkrNetWrapper
from classes.gmail_wrapper import GmailWrapper


def initialize_data():
    folder_with_excels = input(f'Введите имя папки с эксель-файлами с адресами для рассылки:\r\n')
    # folder_with_excels = 'excels'
    excel_files_sequence = FilesSequence(folder=folder_with_excels, files_template='*.xlsx')

    folder_with_attachments = input(f'Введите имя папки с файлами, которые мы будем прикреплять:\r\n')
    # folder_with_attachments = 'attachments'
    attachment_files_sequence = FilesSequence(folder=folder_with_attachments)

    mail_content_file = input(f'Введите имя файла с темой и текстом письма:\r\n')
    # mail_content_file = 'text.docx'
    mail_content_doc = docx.Document(mail_content_file)
    mail_template = MailTemplate(doc=mail_content_doc, attachment_files_sequence=attachment_files_sequence)

    # print(f'\r\n{mail_template}')

    return {'excel_files_sequence': excel_files_sequence,
            'attachment_files_sequence': attachment_files_sequence,
            'mail_template': mail_template}


def order_files_sequence(files_sequence: FilesSequence):
    while True:
        print(f'\r\nПоследовательность файлов из папки {files_sequence.folder}:\r\n{files_sequence}\r\n')
        initial_position = input('Если хотите передвинуть файл - введите его номер и нажмите энтер.\r\n'
                                 'Если текущий порядок устраивает - просто нажмите энтер.\r\n')
        if initial_position == '':
            break

        new_position = input('Введите на какую позицию хотите передвинуть файл:\r\n')
        try:
            files_sequence.reorder_files(current_index=int(initial_position), new_index=int(new_position))
        except IndexError:
            print('Неправильный ввод, повторите снова.\r\n')


def get_emails_from_excel_files_sequence(excel_files_sequence: FilesSequence):
    emails_list = []
    for file in excel_files_sequence.files:
        df = pd.read_excel(file, skiprows=1)

        # Take only email column and remove all blank values
        df = df['Email'][df['Email'].notna()]

        emails_list += df.values.tolist()
        print(f'{len(df.values)} адресов найдено в файле {file}')

    print(f'Всего адресов найдено: {len(emails_list)}\r\n')
    return emails_list


def get_credentials():
    # login, password = 'vladislav_vladislavovich@ukr.net', 'DctvGhbdtn'

    login = input('Введите логин:\r\n')
    password = input('Введите пароль:\r\n')

    return {'login': login, 'password': password}


if __name__ == '__main__':
    data_from_disk = initialize_data()

    order_files_sequence(data_from_disk['attachment_files_sequence'])
    order_files_sequence(data_from_disk['excel_files_sequence'])

    emails_list = get_emails_from_excel_files_sequence(data_from_disk['excel_files_sequence'])

    driver = UkrNetWrapper(config=get_credentials())
    # driver = GmailWrapper(config=get_credentials())

    driver.log_in()

    spammed_mails = []
    for recipient in emails_list:
        mail = Mail(recipient=recipient, mail_template=data_from_disk['mail_template'])
        # driver.send_mail(mail)
        spammed_mails.append(mail.recipient)
        print(f'Mail to {mail.recipient} sent')

    file_name = 'spammed_emails.xlsx'
    spammed_mails_df = pd.DataFrame(data=spammed_mails, columns=['Email'])
    spammed_mails_df.to_excel(file_name)
    print(f'File {file_name} saved')



