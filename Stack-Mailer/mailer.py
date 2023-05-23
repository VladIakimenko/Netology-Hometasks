import os
import smtplib
import imaplib
import atexit

import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


class Mailer:
    def __init__(self,
                 smtp="smtp.gmail.com",
                 imap="imap.gmail.com",
                 smtp_port=587,
                 dotenv_path='.env'):
        self.smtp = smtp
        self.imap = imap
        self.smtp_port = smtp_port
        self.dotenv_path = dotenv_path

        if os.path.exists(self.dotenv_path):
            load_dotenv(self.dotenv_path)
        self.login = os.environ.get("LOGIN")
        self.password = os.environ.get("PASSWORD")
        self.smtp_client = smtplib.SMTP(self.smtp, self.smtp_port)
        self.imap_client = imaplib.IMAP4_SSL(self.imap)
        atexit.register(self.terminate)

    def terminate(self):
        self.smtp_client.quit()

    def send_mail(self, recipients, message, subject=''):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        self.smtp_client.ehlo()
        self.smtp_client.starttls()
        self.smtp_client.ehlo()
        self.smtp_client.login(self.login, self.password)
        self.smtp_client.sendmail(from_addr=self.login,
                                  to_addrs=recipients,
                                  msg=msg.as_string())

    def receive_mail(self, header=None):
        self.imap_client.login(self.login, self.password)
        self.imap_client.list()
        self.imap_client.select("inbox")
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = self.imap_client.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = self.imap_client.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        self.imap_client.logout()
        return email_message
