from parsers.website.proxy_plugin import ProxyPlugin

from controller.website.price.deliveroo import DeliverooPriceController
from controller.website.price.dominos import DominosController
from controller.website.promo.uber_eats import UberEatsPromoController

if __name__ == '__main__':
    # ProxyPlugin()
    # DeliverooPriceController()

    # not work proxy
    # DominosController()

    UberEatsPromoController()
