#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from pathlib import Path
from os import access, R_OK
import utils.logger as l

def file_readable(file):
    """
    :Param path to a file
    check if file is readable
    """
    assert(access(file, R_OK)), f"File {file} is not readable"
    return file

def parse_config():
    """
    Parse config main function
    :Return config
    """
    config = configparser.ConfigParser()
    paths = ["config/sympa.conf", "~/.config/sympa.conf", \
        "/etc/sympa_pymanage/sympa.conf"]
    for p in paths:
        path = Path(p)
        if path.is_file():
            p = file_readable(p)
            config.read(p)
            break
    return config

def try_read_val(config, key, section):
    """
    :Param configuration content, key, section
    :Return value
    """
    try:
        val = config[section][key]
    except Exception as e:
        val = None
        l.logger.error("Value {} in {} does not seem to exist: {}".format(key, section, e))
    return val

def try_read_int(config, key, section):
    """
    :Param configuration content, key, section
    :Return value
    """
    try:
        val = config.getint(section, key)
    except Exception as e:
        val = None
        l.logger.error("Value {} in {} does not seem to exist: {}".format(key, section, e))
    return val