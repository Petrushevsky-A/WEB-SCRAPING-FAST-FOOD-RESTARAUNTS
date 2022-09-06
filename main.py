

# from parser.address.google_maps.google_maps import parse

# from parser.promo.hotukdeals.hotukdeals import *
import time

from parsers.promo.hotukdeals.hotukdeals import HotukdealsParser

from controller.hotukdeals import HotukdealsController
from database.database import DataBase
from cleaner.hotukdeals.hotukdeals import HotukdealsCleaner

import os


if __name__ == '__main__':
    # python 3.10
    HotukdealsController()