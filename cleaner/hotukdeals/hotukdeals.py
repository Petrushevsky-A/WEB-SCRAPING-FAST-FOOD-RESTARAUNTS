
import re
from lxml import html
class HotukdealsCleaner():

    def __init__(self):

        pass


    def get_url_voucher_page(self, data_html):
        # globals
        # Ugreedy
        # multiline
        # href = "(https:\/\/www.hotukdeals\.com\/.*)"
        # $x('//article[contains(@class, "voucher")]//a[@class="js-thread-title"]').map(i => i.textContent)
        # $x('//article[contains(@class, "voucher")]//a[@class="js-thread-title"]').map(i= > i.getAttribute('href'))
        # некоторые карточки содержат только visit ссылки которые открывают сайт BK

        tree = html.fromstring(data_html)
        element = tree.xpath('//a[@class="js-thread-title"]')
        return [i.attrib['href'] for i in element]

    def get_url_deals_page(self, data_html):
        # globals
        # Ugreedy
        # multiline
        # href = "(https:\/\/www.hotukdeals\.com\/.*)"

        tree = html.fromstring(data_html)
        element = tree.xpath('//a[contains(@class, "title")]')
        return [i.attrib['href'] for i in element]


