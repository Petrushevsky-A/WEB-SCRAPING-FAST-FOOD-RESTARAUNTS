import setting

import os
import zipfile

class ProxyPlugin():

    def __init__(self):
        self.PROXY_HOST, self.PROXY_PORT, self.PROXY_USER, self.PROXY_PASSWORD = setting.PROXY.values()
        self.generate_plugin_scripts()
        self.generate_plugin_file()


    def generate_plugin_scripts(self):

        self.manifest_json = r"""
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"23.0.0"
        }
        """

        self.background_js = r"""
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["localhost"]self.
                }
              };
    
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
    
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (self.PROXY_HOST, self.PROXY_PORT, self.PROXY_USER, self.PROXY_PASSWORD)

    def generate_plugin_file(self):
        proxy_plugin_file = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(proxy_plugin_file, 'w') as zp:
            zp.writestr("manifest.json", self.manifest_json)
            zp.writestr("background.js", self.background_js)




