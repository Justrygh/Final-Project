from browsermobproxy import Server
import os
from selenium import webdriver
import urllib.parse as urlparse

chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
firefox_binary = '/root/Desktop/other/firefox_80/firefox'

class Proxy:

    def __init__(self):
        self.path = None
        self.proxy = None
        self.proxy_server = None
        self.driver = None

    def create_server(self):
        """
        :return:
        """
        print("=====> Creating New Server - Please Wait... <=====")
        self.proxy_path()
        self.proxy_server = Server(self.path)
        self.proxy_server.start()
        self.proxy = self.proxy_server.create_proxy()

    def proxy_path(self):
        proxy_path = os.getcwd()
        proxy = ["..", "..", "browsermob-proxy-2.1.4", "bin", "browsermob-proxy"]
        for path in proxy:
            proxy_path = os.path.join(proxy_path, path)
        self.path = proxy_path

    def close_server(self):
        print("=====> Closing the Server - Please Wait... <=====")
        self.proxy.close()
        self.proxy_server.stop()

    def chrome_browser(self,system):
        print("=====> Configuring Chrome Web Driver - Please Wait... <=====")
        path = os.path.join(os.getcwd(), "..", "..", "drivers", "chromedriver")
        url = urlparse.urlparse(self.proxy.proxy).path
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server={0}".format(url))
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--incognito')
        if system.tostring() == "Windows":
            path = path + ".exe"
            chrome_options.binary_location = chrome_path
        else:
            chrome_options.add_argument('--no-sandbox')

        self.driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)

    def firefox_browser(self,system):
        print("=====> Configuring Firefox Web Driver - Please Wait... <=====")
        path = os.path.join(os.getcwd(), "..", "..", "drivers", "geckodriver")
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        profile.set_preference("browser.privatebrowsing.autostart", True)
        selenium_proxy = self.proxy.selenium_proxy()
        profile.set_proxy(selenium_proxy)
        if system.tostring() == "Windows":
            path = path + ".exe"
        self.driver = webdriver.Firefox(executable_path=path, firefox_profile=profile, firefox_binary=firefox_binary)

    def get_driver(self):
        return self.driver

    def get_proxy(self):
        return self.proxy

