#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import ssl
from email.mime.text import MIMEText
import socket
import getpass
from utils import parse_config as cfg
from utils import validate_options as v
import utils.logger as l


def send(to, subject, content, signature, email_send_method="local", \
    smtp_server=None, smtp_port=465, smtp_sender=None, smtp_password=None):

    """Send email to manage sympa list

    :param to: email addresses to send to; should be the email of sympa mail server
    :param subject: the subject
    :param msg: full process information in json
    :param email_send_method: "local" or "custom" (see config file)
    :param smtp_server smtp server to use
    :param smtp_port server port to use
    :param smtp_password your mail password
    :param smtp_sender "From: <user@tld.com>" field
    """

    config = cfg.parse_config()

    if not email_send_method:
        email_send_method = cfg.try_read_val(config, 'email_send_method', 'send_method')
    #if email_send_method == "no":
    #    l.logger.warn("Trying to send email but email_send_method is set to no")

    if not smtp_server:
        smtp_server = cfg.try_read_val(config, 'smtp_remote_server', 'send_method')
        if smtp_server:
            smtp_server = v.strip_dquotes(smtp_server)
    if not smtp_port:
        smtp_port = cfg.try_read_int(config, 'smtp_remote_port', 'send_method')
    if not smtp_password:
        smtp_password = cfg.try_read_val(config, 'smtp_password', 'send_method')
        if smtp_password:
            smtp_password = v.strip_dquotes(smtp_password)
   
    host = socket.getfqdn()
    user = getpass.getuser()
    user_at_host = "{}@{}".format(user, host)

    if smtp_sender == "local":
        smtp_sender = user_at_host
    if not smtp_sender:
        smtp_sender = cfg.try_read_val(config, 'smtp_sender', 'send_method')
        if smtp_sender:
            smtp_sender = v.strip_dquotes(smtp_sender)
        else:
            smtp_sender = "{}@{}".format(user, host)

    body = content
    if signature:
        body += '\n\n(Automatically sent by sympa_pymanage program)'
    msg = MIMEText(body)
    msg['Subject'] = "{}".format(subject)
    msg['From'] = smtp_sender
    if not isinstance(to, str):
        msg['To'] = ', '.join(to)
    else:
        msg['To'] = to

    l.logger.info("Subject: {}".format(subject))
    l.logger.info("Body: {}".format(body))
    l.logger.info("Sender: {}".format(smtp_sender))
    l.logger.info("To: {}".format(msg['To']))
    l.logger.info("Sender: {}".format(smtp_sender))
    
    if email_send_method == "local":
        # Send the message via our own SMTP server.
        with smtplib.SMTP('localhost') as server:
            l.logger.info('Sending email to: {}'.format(msg['To']))
            server.send_message(msg)
    else:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            l.logger.info('Sending email to: {}'.format(msg['To']))
            server.login(smtp_sender, smtp_password)
            server.send_message(msg)
    