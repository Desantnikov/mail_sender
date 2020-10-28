# parse mail theme and mail text from specified *.doc file

# specify files to attach

# take all names of *.xlsx files from specified folder (save to list)
# read files one by one
    # check if 'EMAIL' column present in file
    # read all emails to tuple, add tuple to dict {file_name: emails1, ...}
    # print name of file and amount of emails red
# specify files order (create tuple with names in order)

# send mail (reuse code)


import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH

from classes import MailTemplate


# mail_content_file = input(f'Введите имя файла с темой и текстом письма ')
mail_content_file = 'text.docx'

mail_content_doc = docx.Document(mail_content_file)

mail_template = MailTemplate(mail_content_doc)

print(f'Письмо: \r\n\r\n{mail_template}')

# folder_with_excels = input(f'Введите имя папки с эксель-файлами с адресами для рассылки:\r')
folder_with_excels = 'text.docx'
print('qwdqwd')

input()




# with open("test.txt") as f:


