# proxy plugin generator
from parsers.website.proxy_plugin import ProxyPlugin


# =====================Aggregators===================
# new script
from controller.website.price.deliveroo import DeliverooPriceController
# dominos does not work with the current proxy
# i used vpn ireland for dominos
from controller.website.price.dominos import DominosController

from controller.website.promo.uber_eats import UberEatsPromoController
from controller.website.price.uber_eats import UberEatsPriceController

# =======================Promo=======================
from parsers.website.promo.burger_king.burgerking import start_burgerking_promo
from parsers.website.promo.gmail.gmail import start_gmail_promo
from parsers.website.promo.greggs.greegs import start_greegs_promo
# from parsers.website.promo.hotukdeals.hotukdeals_parser import HotukdealsParser
from parsers.website.promo.just_eats.just_eats import start_just_eats_promo
# from parsers.website.promo.kfc.kfc import start_kfc_promo
from parsers.website.promo.starbucks.starbucks import start_startuck_promo
from parsers.website.promo.mcdonalds.mcdonalds import McDonaldsPromoParser
from parsers.website.promo.deliveroo.deliveroo import start_deliveroo_promo
from controller.website.promo.dominos import DominosPromoController
# ======================Price=========================
from parsers.website.price.just_eats.just_eats import start_just_eats_price
from parsers.website.price.nandos.nandos import start_nandos_price
from parsers.website.price.burger_king.burger_king import start_burger_king_price

if __name__ == '__main__':
    # the class generates a plugin for working with proxies with authenticator
    ProxyPlugin()

    # ===============Aggregators=================
    # DeliverooPriceController()
    # start_deliveroo_promo()

    # not work current proxy
    # DominosController()

    # this site is the most difficult to collect data.
    # it is better to collect data using prepared URLs, since the result is not deterministic when crawling
    # (crawling is different from scraping)
    # new script in development
    # UberEatsPromoController()
    # in the future, it is planned to optimize and speed up the script
    # UberEatsPriceController()

    # ==================Promo====================
    # start_burgerking_promo()
    # DominosPromoController()
    # =============================
    # -------------process repair---------------start_gmail_promo()
    # =============================
    # start_greegs_promo()
    # start_just_eats_promo()
    # =====================
    # ----------process repair------------start_kfc_promo()
    # ====================
    # start_startuck_promo()
    # McDonaldsPromoParser()


    # ==================Price====================
    # start_just_eats_price()
    # ----------process repair----------- start_nandos_price()
    # ----------process repair------------ start_burger_king_price()

