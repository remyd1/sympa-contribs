# Sympa Manage

This is a basic python client program to send emails as a mailing list admin to the sympa server.

You can see a list of commands available [here](https://lists.sympa.community/help/commands.html).

It is not using [sympa SOAP API](https://www.sympa.community/manual/customize/soap-api.html), which, unfortunately, does not seem to be very actively used nowadays.

Use it to ADD, DEL user or send STATS or REVIEW commands.

## Requirements

[`Typer`](https://typer.tiangolo.com/) python library.


## Configuration

You need either a working MTA (eg. [_basic SMTP configuration working with Postfix_](http://www.postfix.org/BASIC_CONFIGURATION_README.html)), or a user/password configuration from an email provider.

Whatever the solution you use, the email sender must have admin permissions on the admin list. You can check logs in the sympa server to see what mail address is used.


Every configuration must be set in `config/sympa.conf`.

## Installation

Clone that directory, and install the requirements in a virtualenv :

```bash
python3 -m venv sympa_venv
source sympa_venv/bin/activate
python3 -m pip install typer
```


## Basic usage

Help :

```bash
#source sympa_venv/bin/activate
python3 sympa_manage.py --help
```

Review :

```bash
python3 sympa_manage.py -m my-list@lists.sympa.community
# same as the following (REVIEW is the default):
python3 sympa_manage.py REVIEW -m my-list@lists.sympa.community
```

Add :

```bash
python3 sympa_manage.py "QUIET ADD" -m my-list@lists.sympa.community -u "john.doe@domain.tld John Doe"
# you repeat -u option as much as you want
python3 sympa_manage.py "QUIET ADD" -m my-list@lists.sympa.community -u "john.doe@domain.tld John Doe" -u jane.doe@domain.tld
```

Delete :

```bash
python3 sympa_manage.py DEL -m my-list@lists.sympa.community -u john.doe@domain.tld 
```