#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Start shuffle mode on a Samsung Frame TV using the SamsungTVWS API. '''

# @ref: https://github.com/NickWaterton/samsung-tv-ws-api

import os
import logging
os.sys.path.append('../')
from samsungtvws import SamsungTVWS

TV_IP = "192.168.178.41"

# Increase debug level
logging.basicConfig(level=logging.INFO)

tv = SamsungTVWS(host=TV_IP)
# Switch art mode on or off
tv.art().set_slideshow_status(True) #

info = tv.art().get_photo_filter_list()
logging.info(info)