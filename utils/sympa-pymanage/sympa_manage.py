#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typer
from typing import Optional
from typing import List
from typing_extensions import Annotated

import utils.logger as l
from utils import bcolors as bc
from utils import parse_config as cfg
from utils import validate_options as v
from utils import email_format as ef

import utils.email as ue


def text_info(action, mailinglist, usermail):
    """
    Just a basic info displayed
    """
    if usermail:
        for um in usermail:
            print(u"\N{check mark} Ok, this program will try your action '{}', on mailing list '{}' for user '{}'".\
                format(action, mailinglist, um))
    else:
        print(u"\N{check mark} Ok, this program will try your action '{}', on mailing list '{}'".\
            format(action, mailinglist))
        print("Default action is a basic REVIEW command.")
        

def main(action: Annotated[str, typer.Argument(help = \
    "The sympa command to use (eg: QUIET ADD)")] = "REVIEW", \
    mailinglist: Annotated[str, typer.Option("--mailinglist", "-m", help = \
    "The mailing list where the action is performed")] = None,
    usermail: Annotated[Optional[List[str]], typer.Option("--usermail", "-u")] \
    = None, msgkey: Annotated[str, typer.Option("--key", "-k", help = \
    "message key index")] = None):
    """
    sympa_pymanage program
    Parse options and do mail actions
    """

    config = cfg.parse_config()
    from_addr = None
    email_to = None
    confirmation_recipient_to = None

    #CUSTOM = False

    list_of_sympa_commands = [ \
        "HELP", "LISTS", "WHICH", "CONFIRM", "QUIT", \
        "INFO", "REVIEW", "SUBSCRIBE", "INVITE", "UNSUBSCRIBE", "SET", \
        "INDEX", "GET", "LAST", "ADD", "QUIET ADD", "DEL", "QUIET DEL", \
        "STATS", "REMIND", "DISTRIBUTE", "REJECT", "MODINDEX" ]
    sympa_set_subcommands = ["NOMAIL", "DIGEST", "DIGESTPLAIN", \
        "SUMMARY", "NOTICE", "MAIL", "CONCEAL", "NOCONCEAL"]


    action = action.upper()

    if action not in list_of_sympa_commands:
        typer.secho("Action command does dot seem to be a valid sympa command !\n\n\
            Please check https://lists.sympa.community/help/commands.html\n", \
            fg=typer.colors.RED)
        raise typer.Exit()

    if mailinglist is None:
        if action not in ["HELP", "LISTS", "WHICH", "CONFIRM"]:
            typer.secho("mailinglist name is required for your command !\n\n\
                Please check https://lists.sympa.community/help/commands.html\n", \
                fg=typer.colors.RED)
            raise typer.Exit()
        mailinglist = ""

    sympa_addr = cfg.try_read_val(config, 'sympa_mail', 'general')
    if not sympa_addr:
        typer.secho("Sympa mail server address is mandatory. See `config/sympa.conf`", \
            fg=typer.colors.RED)
        raise typer.Exit()

    confirmation = cfg.try_read_val(config, 'confirmation', 'general')
    confirm_vals = ['yes', 'Yes', 'YES', 'true', 'True', 'TRUE', 'ok', 'OK', 'Ok']
    if confirmation in confirm_vals:
        confirmation_recipient = cfg.try_read_val(config, 'confirmation_recipient', 'general')
        if confirmation_recipient:
            confirmation_recipient_to = confirmation_recipient.split(",")
            confirmation_recipient_to = v.check_emails(confirmation_recipient_to)

    email_send_method = cfg.try_read_val(config, 'email_send_method', 'send_method')
    if email_send_method in ["yes", "default", "custom"]:
        #CUSTOM = True
        email_to = cfg.try_read_val(config, 'smtp_receiver', 'send_method')
        if email_to:
            email_to = email_to.split(",")
            email_to = v.check_emails(email_to)
        alt_from = cfg.try_read_val(config, 'smtp_sender', 'send_method')
        if alt_from:
            from_addr = v.check_emails(alt_from)
    else:
        alt_from = cfg.try_read_val(config, 'receiver', 'general')
        if alt_from:
            from_addr = v.check_emails(alt_from)
        else:
            from_addr = "local"
    
    text_info(action, mailinglist, usermail)
    ef.send_email(sympa_addr, action, usermail, mailinglist, \
        confirmation_recipient_to, from_addr, email_to, email_send_method)


if __name__ == "__main__":
    typer.run(main)
