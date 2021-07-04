import asyncio
from email.parser import BytesParser, Parser
from email.policy import default

import smtplib
import logging
import imaplib

import quopri
import base64

import email
from email.message import EmailMessage

content = 'Hello world! It was sent by using python!'
subject = 'Try with EmailMessage'


def run(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed)
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport) -> None:
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        message = data
        print('Data received: {}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


class Client:

    def __init__(self, send_port, read_port, host, from_addr, to_addr, password):
        self.send_port = send_port
        self.read_port = read_port
        self.host = host
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.password = password

    def _make_message(self, content, subject):
        msg = EmailMessage()
        msg.set_content(content)

        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = self.to_addr

        return msg

    def send(self, content, subject=None):
        # connect to mail
        send_host = 'smtp.{}'.format(self.host)
        server = smtplib.SMTP_SSL(host=send_host, port=self.send_port)
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)

        # make and send message
        msg = self._make_message(content, subject)
        server.send_message(msg)
        server.quit()

    def get_first_text_block(self, email_message_instance):
        pass

    @staticmethod
    def _download_attachment(email_message):
        # downloading attachment
        for number, part in enumerate(email_message.walk()):
            print(part.get_payload())
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            file_name = part.get_filename()
            print('read file : {file_name}'.format(file_name=file_name))
            with open(f'download_{number}_file', 'wb') as fp:
                fp.write(part.get_payload(decode=True))

    def _convert_mail_to_str(self, raw_email: str):
        # convert to work with mail
        email_message = email.message_from_string(raw_email)
        self._download_attachment(email_message)

        return email_message['From']

    def read(self):
        # connect to server
        read_host = 'imap.{}'.format(self.host)
        imap_server = imaplib.IMAP4_SSL(host=read_host, port=self.read_port)
        imap_server.login(self.from_addr, self.password)
        imap_server.select()

        # Find all emails in inbox and print out the raw email data
        # _, message_numbers_raw = imap_server.search(None, 'All')
        _, message_numbers_raw = imap_server.search(None, 'FROM', '"RTrader"')
        for message_number in [message_numbers_raw[0].split()[0]]:
            _, msg = imap_server.fetch(message_number, '(RFC822)')
            try:
                raw_email = quopri.decodestring(msg[0][1]).decode()
                email_message = self._convert_mail_to_str(raw_email)
                print("Message %s\n %s\n" % (message_number, email_message))
            except UnicodeDecodeError:
                raw_email = msg[0][1].decode()
                email_message = self._convert_mail_to_str(raw_email)
                print("Message %s\n %s\n" % (message_number, email_message))

        imap_server.close()
        imap_server.logout()


# def run():
#     msg = EmailMessage()
#     msg.set_content(content)
#
#     msg['Subject'] = subject
#     msg['From'] = fromaddrs
#     msg['To'] = toaddrs
#
#     logger.info('connect to mail')
#     # server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
#     server = smtplib.SMTP_SSL('127.0.0.1', 8887)
#
#
#     logger.info('loggin to my mail')
#     # server.login(fromaddrs, password)
#
#     logging.info('set debug')
#     server.set_debuglevel(1)
#
#     logging.info('send mail')
#     server.send_message(msg)
#     server.quit()


if __name__ == '__main__':
    run('127.0.0.1', 8887)

