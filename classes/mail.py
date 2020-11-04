import smtplib
import ssl
import os
import logging
from classes.files_sequence import FilesSequence
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self, smtp_url: str, smtp_port: int, sender_email: str, sender_password: str, body: str, subject: str,
                 files_to_attach_sequence: FilesSequence, logger=logging.getLogger('Mail')):
        self.logger = logger

        self.smtp_url = smtp_url
        self.smtp_port = smtp_port

        self.sender_email = sender_email
        self.sender_password = sender_password

        self._initialize_message(sender_email=sender_email, subject=subject, message_body=body)

        [self._attach_file(path=path) for path in files_to_attach_sequence.paths_list]

        self.logger.info(f'Mail created:\n{self}')

    def __str__(self):
        return '\n'.join([f'{k}: {v}' for k, v in self.__dict__.items()])

    def _initialize_message(self, sender_email: str, subject: str, message_body: str):
        self.message = MIMEMultipart("alternative")
        self.message["From"] = sender_email
        self.message["Subject"] = subject
        self.message.attach(MIMEText(message_body, "html", "utf-8"))

    def _attach_file(self, path):
        with open(path, "rb") as file_to_attach:
            part = MIMEApplication(file_to_attach.read(), Name=os.path.basename(path))

        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'
        self.message.attach(part)

    def send_to(self, receiver_email: str):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_url, self.smtp_port, context=context) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, self.message.as_string().encode('ascii'))
        self.logger.info(f'Mail to {receiver_email} sent')
