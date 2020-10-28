# save used mail to list
import docx
import pandas as pd

from classes.file_classes import FilesSequence
from classes.mail_classes import MailTemplate, Mail
from classes.ukr_net_wrapper import UkrNetWrapper

# folder_with_excels = input(f'Введите имя папки с эксель-файлами с адресами для рассылки:\r')
folder_with_excels = 'excels'
excel_files_sequence = FilesSequence(folder=folder_with_excels, files_template='*.xlsx')

# folder_with_attachments = input(f'Введите имя папки с файлами, которые мы будем прикреплять:\r')
folder_with_attachments = 'attachments'
attachment_files_sequence = FilesSequence(folder=folder_with_attachments)

# mail_content_file = input(f'Введите имя файла с темой и текстом письма ')
mail_content_file = 'text.docx'
mail_content_doc = docx.Document(mail_content_file)
mail_template = MailTemplate(doc=mail_content_doc, attachment_files_sequence=attachment_files_sequence)

print(f'\r\n{mail_template}')


# # ordering excel files to collect emails from
# while True:
#     print(f'\r\nПоследовательность файлов:\r\n{excel_files_sequence}\r\n')
#     initial_position = input('Если хотите передвинуть файл - введите его номер и нажмите энтер.\r\n'
#                              'Если текущий порядок устраивает - просто нажмите энтер.\r\n')
#     if initial_position == '':
#         break
#
#     new_position = input('Введите на какую позицию хотите передвинуть файл:\r\n')
#     try:
#         excel_files_sequence.reorder_files(current_index=int(initial_position), new_index=int(new_position))
#     except IndexError:
#         print('Неправильный ввод, повторите снова.\r\n')

# # ordering attachment files
# while True:
#     print(f'\r\nПоследовательность файлов:\r\n{attachment_files_sequence}\r\n')
#     initial_position = input('Если хотите передвинуть файл - введите его номер и нажмите энтер.\r\n'
#                              'Если текущий порядок устраивает - просто нажмите энтер.\r\n')
#     if initial_position == '':
#         break
#
#     new_position = input('Введите на какую позицию хотите передвинуть файл:\r\n')
#     try:
#         attachment_files_sequence.reorder_files(current_index=int(initial_position), new_index=int(new_position))
#     except IndexError:
#         print('Неправильный ввод, повторите снова.\r\n')

emails_list = []
for file in excel_files_sequence.files:
    df = pd.read_excel(file, skiprows=1)

    # Take only email column and remove all blank values
    df = df['Email'][df['Email'].notna()]

    emails_list += df.values.tolist()

    print(f'{len(df.values)} адресов найдено в файле {file}')
    print(f'Всего адресов найдено: {len(emails_list)}\r\n')


# login = input('Введите логин:\r\n')
# password = input('Введите пароль:\r\n')

login, password = 'vladislav_vladislavovich@ukr.net', 'DctvGhbdtn'
config = {'login': login, 'password': password}

driver = UkrNetWrapper(config=config)

# log into ukr net
driver.log_in()

# send mails to all recipients
for recipient in emails_list:
    mail = Mail(recipient=recipient, mail_template=mail_template)
    driver.send_mail(mail)


# attach_files_button.send_keys(r'C:\Users\anton.desiatnykov\PycharmProjects\mail_sender\classes\file_classes.py')
# click on "attach files"
# driver.wait_and_send_keys('//*[@id="screens"]/div/div[2]/section[2]/div[2]/label/button', keys=r'C:\Users\anton.desiatnykov\PycharmProjects\mail_sender\classes\file_classes.py')
print('asd')


print('qwdqwd')

input()




# with open("test.txt") as f:


