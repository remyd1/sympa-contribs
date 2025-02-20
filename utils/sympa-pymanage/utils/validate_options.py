#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils.logger as l
import re
import sys

def strip_dquotes(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found,
    or there are less than 2 characters, return the string unchanged.
    """
    if (len(s) >= 2 and s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s

def check_emails(emails):
    """
    Basic email check with regexp
    param str or list of emails
    return list of valid emails
    """
    
    regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    
    if isinstance(emails, str):
        email = emails.strip()
        email = strip_dquotes(email)
        if not re.fullmatch(regex, email):
            sys.exit("Not a good mail format")
        return email
    
    else:
        sanitized_emails = []
        for email in emails:
            email = email.strip()
            email = strip_dquotes(email)
            if not re.fullmatch(regex, email):
                emails.remove(email)
            else:
                sanitized_emails.append(email)
        return sanitized_emails