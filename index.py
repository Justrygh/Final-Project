from browsermobproxy import Server
from selenium import webdriver
import json
import urllib.parse as urlparse
import uuid
from database import DNSDatabase
from ping3 import ping
from dns_timings import measure_dns
import re
import subprocess
from subprocess import call, run, PIPE
import platform
import windows
import linux
import os


def create_server():
    """ Configure Server """
    print("=====> Creating New Server - Please Wait... <=====")
    server = Server(configure_proxy())
    server.start()
    proxy = server.create_proxy()
    return proxy, server


def configure_proxy():
    """ Configure Proxy Server (BrowserMob Proxy) """
    proxy_path = os.getcwd()  # path to firefox web driver
    proxy = ["browsermob-proxy-2.1.4", "bin", "browsermob-proxy"]
    for path in proxy:
        proxy_path = os.path.join(proxy_path, path)
    return proxy_path


def chrome_browser(proxy):
    """ Configure Chrome Web Driver for Windows """
    chrome_driver = os.path.join(os.getcwd(), "chromedriver")
    url = urlparse.urlparse(proxy.proxy).path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={0}".format(url))
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)
    return driver


def firefox_browser(proxy):
    """ Configure Firefox Web Driver """
    path = os.path.join(os.getcwd(), "geckodriver")
    profile = webdriver.FirefoxProfile()
    selenium_proxy = proxy.selenium_proxy()
    profile.set_proxy(selenium_proxy)
    driver = webdriver.Firefox(executable_path=path, firefox_profile=profile)
    return driver


def configure_database():
    """ Configure Database - PostgreSQL """
    db = DNSDatabase.init_from_config_file('postgres.ini')
    db._connect()
    return db


def configure_websites():
    """ Configure Websites """
    webs = open("websites.txt", "r")
    websites = webs.read().split('\n')
    if websites[-1] == '':
        del websites[-1]
    webs.close()
    return websites


def convert_recursive(resolver):
    """ Recursive - Name of the Resolver """
    recursive = None
    if resolver == "1.1.1.1":
        recursive = "Cloudflare"
    elif resolver == "8.8.8.8":
        recursive = "Google"
    elif resolver == "9.9.9.9":
        recursive = "Quad9"
    return recursive


def convert_resolver(resolver):
    """ Resolver for DoH - convert ip to url """
    if resolver == "1.1.1.1":
        resolver = "https://cloudflare-dns.com/dns-query"
    elif resolver == "8.8.8.8":
        resolver = "https://dns.google/dns-qeury"
    elif resolver == "9.9.9.9":
        resolver = "https://dns.quad9.net/dns-query"
    return resolver


def ping_resolver(resolver_ip, count=5):
    """ Send "count" pings """
    delays = []
    for i in range(count):
        try:
            d = ping(resolver_ip, unit='ms')
            if d:
                delays.append(d)
        except Exception as e:
            print('ping error:', e)
            return []
    return delays


def configure_server(proxy):
    """ The Experiment - HAR + DNS """
    database, resolver, recursive, websites, browsers, dns_type, delay, operation_system = container()
    for browser in browsers:
        experiment = uuid.uuid1()
        print("=====> Configuring Server - Please Wait... <=====")
        if browser == "Chrome":
            driver = chrome_browser(proxy)
            print("=====> Using Google Chrome <=====")
        elif browser == "Firefox":
            driver = firefox_browser(proxy)
            print("=====> Using Firefox <=====")
        for dns in dns_type:
            if dns == "dot":
                configure_stubby(resolver, operation_system)
            for website in websites:
                har_uuid = uuid.uuid1()
                print("===========================================================")
                print("Type: ", dns, " | Resolver: ", recursive)
                print("Creating HAR for Website: https://{}".format(website))
                proxy.new_har("https://{}".format(website), options={'captureHeaders': True})
                driver.get("https://{}".format(website))
                har = json.loads(json.dumps(proxy.har))
                rv = database.insert_har(experiment, website, browser, recursive, operation_system, dns, har, har_uuid, None, delay)
                if not rv:
                    print("Saved HAR for website {}".format(website))
                if dns == "doh":
                    resolver = convert_resolver(resolver)
                try:
                    dns_info = measure_dns(website, har, dns, resolver)
                    if dns_info:
                        rv_dns = database.insert_dns(har_uuid, experiment, browser, recursive, operation_system, dns, dns_info)
                        if not rv_dns:
                            print("Saved DNS for website {}".format(website))
                            print("===========================================================\n")
                    else:
                        print("===========================================================\n")
                except:
                    print("An exception occurred! Please try again later.")

            if dns == "dot":
                close_stubby(resolver, operation_system)
        driver.quit()


def container():
    """ Configuration Container"""
    operation_system = platform.system()
    database = configure_database()
    websites = configure_websites()
    dns_type = ["dns", "dot", "doh"]
    if platform.system() == "Windows":
        resolver, browsers = windows.container()
    elif platform.system() == "Linux":
        resolver, browsers = linux.container()
    recursive = convert_recursive(resolver)
    delay = ping_resolver(resolver)
    return database, resolver, recursive, websites, browsers, dns_type, delay, operation_system


def configure_stubby(resolver, operation_system):
    if operation_system == "Windows":
        windows.configure_stubby(resolver)
    elif operation_system == "Linux":
        linux.configure_stubby(resolver)


def close_stubby(resolver, operation_system):
    if operation_system == "Windows":
        windows.close_stubby(resolver)
    elif operation_system == "Linux":
        linux.close_stubby(resolver)


def close_server(proxy, server):
    """ Close the Server """
    proxy.close()
    server.stop()


def main():
    proxy, server = create_server()
    configure_server(proxy)
    close_server(proxy, server)


if __name__ == "__main__":
    main()
