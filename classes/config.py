from classes.files_sequence import FilesSequence


class Config:
    def __init__(self, args):
        if args.stub:
            self.sender_email = 'vladislav_vladislavovich@ukr.net'
            self.sender_password = 'SIPdGNqgAR4fCJEG'
            self.smtp_url = 'smtp.ukr.net'
            self.smtp_port = 465
            self.subject = 'Subject UKR NET!!!!!'
            self.folder_with_attachments = 'attachments'
            self.text_file_name = 'text.txt'
            self.folder_with_excels = 'excels'
            self.spammed_emails_file = 'spammed_emails.xlsx'

        else:
            self.sender_email = input('Введите адрес с которого отправлять:\r\n')
            self.sender_password = input('Введите пароль:\r\n')
            self.smtp_url = input('Введите адрес SMTP сервера:\r\n') if not args.gmail else 'smtp.gmail.com'
            self.smtp_port = input('Введите порт SMTP сервера:\r\n') if not args.gmail else 465
            self.subject = input('Введите тему письма:\r\n')
            self.folder_with_attachments = input(f'Введите имя папки с файлами, которые мы будем прикреплять:\r\n')
            self.text_file_name = input('Введите название файла с телом письма:\r\n')
            self.folder_with_excels = input(f'Введите имя папки с эксель-файлами с адресами для рассылки:\r\n')
            self.spammed_emails_file = input(f'Введите имя файла с обработанными адресами (создать если нет):\r\n')

        self.files_to_attach_sequence = FilesSequence(folder=self.folder_with_attachments, reorder=not args.no_reorder)

        with open(self.text_file_name) as f:
            self.body = f.read()

    def __str__(self):
        return '\n'.join([f'{k}: {v if k != "body" else f"{v[:30]}..."}' for k, v in self.__dict__.items()])

    def get_mail_settings(self):
        return {'smtp_url': self.smtp_url, 'smtp_port': self.smtp_port,
                'sender_email': self.sender_email,
                'sender_password': self.sender_password,
                'body': self.body, 'subject': self.subject,
                'files_to_attach_sequence': self.files_to_attach_sequence}
