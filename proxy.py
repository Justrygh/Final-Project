from browsermobproxy import Server
import os
from selenium import webdriver
import urllib.parse as urlparse


class Proxy:

    def __init__(self):
        self.path = None
        self.proxy = None
        self.proxy_server = None
        self.driver = None

    def create_server(self):
        """ Configure Server - Creating New Proxy Server """
        print("=====> Creating New Server - Please Wait... <=====")
        self.configure_proxy()
        self.proxy_server = Server(self.path)
        self.proxy_server.start()
        self.proxy = self.proxy_server.create_proxy()

    def configure_proxy(self):
        """ Configure Proxy Server """
        proxy_path = os.getcwd()
        proxy = ["browsermob-proxy-2.1.4", "bin", "browsermob-proxy"]
        for path in proxy:
            proxy_path = os.path.join(proxy_path, path)
        self.path = proxy_path

    def close_server(self):
        """ Close the Server """
        self.proxy.close()
        self.proxy_server.stop()

    def chrome_browser(self):
        """ Configure Chrome Web Driver """
        chrome_driver = os.path.join(os.path.join(os.getcwd(), "drivers"), "chromedriver")
        url = urlparse.urlparse(self.proxy.proxy).path
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server={0}".format(url))
        chrome_options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(chrome_driver, options=chrome_options)

    def firefox_browser(self):
        """ Configure Firefox Web Driver """
        path = os.path.join(os.path.join(os.getcwd(), "drivers"), "geckodriver")
        profile = webdriver.FirefoxProfile()
        selenium_proxy = self.proxy.selenium_proxy()
        profile.set_proxy(selenium_proxy)
        self.driver = webdriver.Firefox(executable_path=path, firefox_profile=profile)

    def get_driver(self):
        return self.driver

