

from controller.hotukdeals import HotukdealsController



from parsers.price.dominos import dominos_2
from parsers.price.dominos.dominos_parser import DominosParser
from cleaner.price.dominos import DominosCleaner
from controller.price.dominos import DominosController
from controller.promo.dominos import DominosPromoController
from controller.promo.uber_eats import UberEatsPromoController


# old scripts price
from parsers.price.just_eats.just_eats import start_just_eats_price
from parsers.price.just_eats.just_eats_v2 import start_just_eats_price_v2
from parsers.price.uber_eats.uber_eats import start_uber_eats_price
from parsers.price.uber_eats.uber_eats_v2 import start_uber_eats_price_v2
from parsers.price.deliveroo.deliveroo import start_deliveroo_price
from parsers.price.deliveroo.deliveroo_v2 import start_deliveroo_price_v2
from parsers.price.nandos.nandos import start_nandos_price
# from parsers.price.nandos.nandos_v2 import start_nandos_price_v2
from parsers.price.supermarcs.supermarcs import SupermarcsPromoParser


# old scripts promo
from parsers.promo.uber_eats.uber_eats import start_uber_eats_promo
from parsers.promo.Starbucks.Starbucks import start_startuck_promo
from parsers.promo.just_eats.just_eats import start_just_eats_promo
from parsers.promo.Greegs.Greegs import start_greegs_promo
from parsers.promo.deliveroo.deliveroo_v2 import start_deliveroo_promo
from parsers.promo.burger_king.burgerking import start_burgerking_promo
from parsers.promo.mcdonalds.mcdonalds import start_mcdonalds_promo
from parsers.promo.kfc.kfc import start_kfc_promo
from parsers.promo.mcdonalds.mcdonalds import McDonaldsPromoParser



from parsers.promo.gmail.gmail import start_gmail_promo


from data_showcase.price import NandosPriceToPriceDB
from data_showcase.price import DeliverooPriceToPiceDB
from data_showcase.price import JustEatsPriceToPiceDB
from data_showcase.price import UberEatsPriceToPiceDB
from data_showcase.promo import DeliverooPromoToPromoDB
from data_showcase.promo import DominosPromoToPromoDB
from data_showcase.promo import JustEatsPromoToPromoDB
from data_showcase.promo import BurgerKingPromoToPromoDB
from data_showcase.promo import StarbucksPromoToPromoDB
from data_showcase.promo import McDonaldsPromoToPromoDB


from controller.price.deliveroo import DeliverooPriceController
if __name__ == '__main__':

    # DominosController()
    # DominosPromoController()
    # DominosCleaner()
    DeliverooPriceController()

    # start_just_eats_price_v2()
    # start_uber_eats_price_v2()
    # start_uber_eats_price()
    # start_deliveroo_price()
    # start_deliveroo_price_v2()
    # SupermarcsPromoParser()

    # start_nandos_price()
    # start_uber_eats_promo()
    # start_startuck_promo()
    # start_just_eats_promo()
    # start_greegs_promo()
    # start_deliveroo_promo()
    # start_burgerking_promo()
    # start_gmail_promo()
    # start_kfc_promo()

    # Витрина данных прайс
    # NandosPriceToPriceDB()
    # DeliverooPriceToPiceDB()
    # JustEatsPriceToPiceDB()
    # UberEatsPriceToPiceDB()

    # Витрина данных промо
    # DeliverooPromoToPromoDB()
    # DominosPromoToPromoDB()
    # JustEatsPromoToPromoDB()
    # BurgerKingPromoToPromoDB()
    # StarbucksPromoToPromoDB()

    # start_mcdonalds_promo()
    # McDonaldsPromoParser()
    # McDonaldsPromoToPromoDB()
    # Текущая разработка
    # UberEatsPromoController().start_parse()
    # UberEatsPromoController()
    pass