
import re
from lxml import html

class HotukdealsCleaner():

    def __init__(self, data_html):

        self.data_html = data_html
        pass


    def get_url_voucher_page(self):
        # globals
        # Ugreedy
        # multiline
        # href = "(https:\/\/www.hotukdeals\.com\/.*)"
        # $x('//article[contains(@class, "voucher")]//a[@class="js-thread-title"]').map(i => i.textContent)
        # $x('//article[contains(@class, "voucher")]//a[@class="js-thread-title"]').map(i= > i.getAttribute('href'))
        # некоторые карточки содержат только visit ссылки которые открывают сайт BK

        url = self.find('//a[contains(@class, "title")]', attribute='attrib', attribute_index='href')
        if (not url) or 'visit' in url[0]:
            return ['Not found', ]
        return url


    def get_url_deals_page(self):
        url = self.find('//a[contains(@class, "title")]', attribute = 'attrib', attribute_index= 'href')
        return url

    def find(self,xpath, attribute = None, method = None, method_arguments = None, attribute_index = None):
        try:
            tree = html.fromstring(self.data_html)
            elements = tree.xpath(xpath)

            # # python 3.10
            # match locals():
            #     case {'attribute': attribute,'attribute_index': attribute_index} if not attribute_index == None:
            #         return [i.__getattribute__(attribute)[attribute_index] for i in elements]
            #     case {'attribute': attribute}:
            #         return [i.__getattribute__(attribute) for i in elements]
            #     case {'method': method ,'method_arguments':method_arguments} if not method_arguments == None:
            #         return [i.__getattribute__(method)(method_arguments) for i in elements]
            #     case {'method': method }:
            #         return [i.__getattribute__(method)() for i in elements]

            # pattern = {k: v for k, v in locals().values() if not v == None}
            pattern = [k for k, v  in locals().items() if not v==None]
            # python 3.10 вариант 2
            match pattern:
                case [*t, 'attribute', 'attribute_index']:
                    return [i.__getattribute__(attribute)[attribute_index] for i in elements]
                case [*t, 'attribute', ]:
                    return [i.__getattribute__(attribute) for i in elements]
                case [*t, 'method', 'method_arguments']:
                    return [i.__getattribute__(method)(method_arguments) for i in elements]
                case [*t, 'method', ]:
                    return [i.__getattribute__(method)() for i in elements]

            # # python 3.9
            # if attribute and attribute_index:
            #     return [i.__getattribute__(attribute)[attribute_index] for i in elements]
            # if attribute:
            #     return [i.__getattribute__(attribute) for i in elements]
            # if method and method_arguments:
            #     return [i.__getattribute__(method)(method_arguments) for i in elements]
            # if method:
            #     return [i.__getattribute__(method)() for i in elements]
        except Exception as ex:
            print(ex)
            return ['Not found', ]

    def clean_voucher_codes(self, data_html):
        head = self.find('//a[contains(@class, "title")]', attribute='attrib', attribute_index='href')
        image = self.find('//a[contains(@class, "title")]', attribute='attrib', attribute_index='href')
        price = self.find('//a[contains(@class, "title")]', attribute='attrib', attribute_index='href')
        code = self.find('//a[contains(@class, "title")]', attribute='attrib', attribute_index='href')
        date = self.find('//a[contains(@class, "title")]', attribute='attrib', attribute_index='href')
        last_used = self.find('//a[contains(@class, "title")]', attribute='attrib', attribute_index='href')
        external_url = self.find('//a[contains(@class, "title")]', attribute='attrib', attribute_index='href')
        more_info = self.find('//a[contains(@class, "title")]', attribute='attrib', attribute_index='href')
        return url

    def clean_deals_cards(self, data_html):
        tree = html.fromstring(data_html)
        element = tree.xpath('//a[contains(@class, "title")]')
        return [i.attrib['href'] for i in element]

