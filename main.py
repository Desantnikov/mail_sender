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

from classes.file_classes import FilesSequence
from classes.mail_classes import MailTemplate

# mail_content_file = input(f'Введите имя файла с темой и текстом письма ')
mail_content_file = 'text.docx'

mail_content_doc = docx.Document(mail_content_file)

mail_template = MailTemplate(doc=mail_content_doc)

print(f'\r\n{mail_template}')

# folder_with_excels = input(f'Введите имя папки с эксель-файлами с адресами для рассылки:\r')
folder_with_excels = 'excels'

files_sequence = FilesSequence(folder=folder_with_excels)

while True:
    print(f'\r\nПоследовательность файлов:\r\n{files_sequence}\r\n')
    initial_position = input('Если хотите передвинуть файл - введите его номер и нажмите энтер.\r\n'
                             'Если текущий порядок устраивает - просто нажмите энтер.\r\n')
    if initial_position == '':
        break

    elif initial_position.isdigit():
        new_position = input('Введите на какую позицию хотите передвинуть файл:\r\n')

        files_sequence.reorder_files(current_index=int(initial_position), new_index=int(new_position))
    else:
        print('Неправильный ввод, повторите снова.\r\n')


print('qwdqwd')

input()




# with open("test.txt") as f:


