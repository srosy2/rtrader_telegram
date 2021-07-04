import smtplib
import logging
import imaplib

import quopri
import base64

import email
from email.message import EmailMessage
from bot import main
from prepare import PrepareMessage

from server import Client
# logging.getLogger().setLevel(logging.INFO)
logger = logging
logger.getLogger().setLevel(logging.INFO)


if __name__ == '__main__':
    main()
    # client = Client(465, 993, 'mail.ru', 'leshhuk.2000@mail.ru', 'leshhuk3@gmail.com', 'Dkflbckfd1!!!!!')
