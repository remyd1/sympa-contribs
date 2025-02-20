#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils.logger as l
import utils.email as ue

def send_email(sympa_addr, action, usermail, mailinglist, \
    confirmation_recipient_to, from_addr, email_to, email_send_method):
    """
    Mail formatting before sending it
    """

    if not usermail:
        body = compute_string(action, "", mailinglist)
        subject = body
    else:
        if len(usermail) > 1:
            """
            Need to concatenate the body to send only one big mail.
            """
            body = ""
            for um in usermail:
                body = body + "\r\n" + compute_string(action, um, mailinglist)
            #subject = "{} on {}".format(action, mailinglist)
            subject = ""
        elif len(usermail) == 1:
            body = compute_string(action, usermail[0], mailinglist)
            subject = body

    body = body + "\r\n" + "QUIT"

    # signature is only added to the confirmation email
    signature = False
    # send mail to the server
    ue.send(sympa_addr, subject, body, signature, email_send_method, None, None, from_addr, None)
    # send optional confirmation to the receiver
    if confirmation_recipient_to or email_to:
        signature = True
        body = "\r\n\
        This is a confirmation mail from sympa_pymanage.\r\n\
        Following command has been sent to the mail server:\r\n\
        {} \r\n".format(action)
        if mailinglist:
            body = body + " \r\n ...With mailinglist: {} \r\n".format(mailinglist)
        if usermail:
            if isinstance(usermail, list):
                body = body + " \r\n ...With usermails: {} \r\n".format(", ".join(usermail))
            else:
                body = body + " \r\n ...With usermail: {} \r\n".format(usermail)

        if confirmation_recipient_to:
            ue.send(confirmation_recipient_to, subject, body, signature, \
                email_send_method, None, None, from_addr, None)
        else:
            ue.send(email_to, subject, body, signature, email_send_method, \
                None, None, from_addr, None)    



def compute_string(action, usermail, mailinglist):
    """
    From https://lists.sympa.community/help/commands.html
    It seems that every moderator or proprietary commands
     look like this format:
    CMD mailinglist <options>
    """
    if not usermail:
        usermail=""
    subject="{} {} {}".format(action, mailinglist, usermail)
    return subject