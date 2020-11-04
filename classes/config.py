from classes.files_sequence import FilesSequence


class Config:
    def __init__(self, stub=False):
        if stub:
            self.data = {'sender_email': '***',
                         'sender_password': '***',
                         'smtp_url': 'smtp.ukr.net',
                         'smtp_port': 465,
                         'subject': 'Subject UKR NET!!!!!',
                         'folder_with_attachments': 'attachments',
                         'text_file_name': 'text.txt',
                         'folder_with_excels': 'excels',
                         'spammed_emails_file': 'spammed_emails.xlsx'
                         }

        else:
            self.data = {'sender_email': input('Введите адрес с которого отправлять:\r\n'),
                         'sender_password': input('Введите пароль:\r\n'),
                         'smtp_url': input('Введите адрес SMTP сервера:\r\n'),
                         'smtp_port': input('Введите порт SMTP сервера:\r\n'),
                         'subject': input('Введите тему письма:\r\n'),
                         'folder_with_attachments': input(
                             f'Введите имя папки с файлами, которые мы будем прикреплять:\r\n'),
                         'text_file_name': input('Введите название файла с телом письма:\r\n'),
                         'folder_with_excels': input(
                             f'Введите имя папки с эксель-файлами с адресами для рассылки:\r\n'),
                         'spammed_emails_file': input(f'Введите имя файла с обработанными адресами '
                                                      f'(создать если отсутствует):\r\n')
                         }

        self.data['files_to_attach_sequence'] = FilesSequence(folder=self.data.pop('folder_with_attachments'),
                                                              reorder_on_creation=not stub)

        with open(self.data.pop('text_file_name')) as f:
            self.data['body'] = f.read()

        # quick w/a
        [setattr(self, k, v) for k, v in self.data.items()]

    def __str__(self):
        return '\n'.join([f'{k}: {v if k != "body" else f"{v[:30]}..."}' for k, v in self.data.items()])
