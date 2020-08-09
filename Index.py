from browsermobproxy import Server
from selenium import webdriver
import os
import json
import urllib.parse as urlparse
import uuid
import platform
from database import DNSDatabase
from ping3 import ping
from dns_timings import measure_dns
import re
from subprocess import call


chrome_driver_path = "C:\\Users\\Computer\\Desktop\\chromedriver.exe" # path to chrome web driver
browsermob_proxy_path = "C:\\Users\\Computer\\Desktop\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat" # path to firefox web driver


def chrome_browser(proxy):
    """Chrome Web Driver"""
    chrome_driver = chrome_driver_path
    url = urlparse.urlparse(proxy.proxy).path
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={0}".format(url))
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)
    return driver


def firefox_browser(proxy):
    """Firefox Web Driver"""
    profile = webdriver.FirefoxProfile()
    selenium_proxy = proxy.selenium_proxy()
    profile.set_proxy(selenium_proxy)
    driver = webdriver.Firefox(firefox_profile=profile)
    return driver


def ping_resolver(resolver_ip, count=5):
    # Send "count" pings
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


def configure_dns():
    resolver = None
    operation_system = platform.system()
    if operation_system == "Windows":
        instructor = open("Instructor_Windows.txt", 'r')
        print(instructor.read())
        p = os.system("netsh interface show interface")
        interface = input("Choose your interface according to your adapter & connection: ")
        resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        p = os.system('netsh interface ip set dns name="{0}" source="static" address="{1}"'.format(interface, resolver))
    elif operation_system == "Linux":
        instructor = open("Instructor_Linux.txt", 'r')
        print(instructor.read())
        resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        p = os.system('echo "nameserver {}" > /etc/resolv.conf'.format(resolver))
    elif operation_system == "Darwin":
        instructor = open("Instructor_Mac.txt", 'r')
        print(instructor.read())
        p = os.system("networksetup listallnetworkservices")
        interface = input("Choose your interface according to your adapter & connection: ")
        resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        p = os.system("networksetup -setdnsservers {0} {1}".format(interface, resolver))
    else:
        print("Error: Our script supports Windows/Linux/Darwin(Mac) Operation Systems Only!")
    return resolver, operation_system


def configure_server(proxy):
    database, resolver, recursive, operation_sys, websites, browsers, dns_type, delay = container()
    for browser in browsers:
        experiment = uuid.uuid1()
        print("=====> Configuring Server - Please Wait... <=====")
        if browser == "Chrome":
            driver = chrome_browser(proxy)
            print("=====> Using Google Chrome <=====")
        if browser == "Firefox":
            driver = firefox_browser(proxy)
            print("=====> Using Firefox <=====")
        for dns in dns_type:
            for website in websites:
                har_uuid = uuid.uuid1()
                print("===========================================================")
                print("Type: ", dns, " | Resolver: ", recursive)
                print("Creating HAR for Website: https://{}".format(website))
                proxy.new_har("https://{}".format(website), options={'captureHeaders': True})
                driver.get("https://{}".format(website))
                har = json.loads(json.dumps(proxy.har))
                rv = database.insert_har(experiment, website, browser, recursive, operation_sys, dns, har, har_uuid, None, delay)
                if not rv:
                    print("Saved HAR for website {}".format(website))
                if dns == "doh":
                    resolver = convert_resolver(resolver)
                try:
                    dns_info = measure_dns(website, har, dns, resolver)
                    if dns_info:
                        rv_dns = database.insert_dns(har_uuid, experiment, browser, recursive, operation_sys, dns, dns_info)
                        if not rv_dns:
                            print("Saved DNS for website {}".format(website))
                            print("===========================================================\n")
                    else:
                        print("===========================================================\n")

                except:
                    print("An exception occurred! Please try again later.")

        driver.quit()


def configure_database():
    db = DNSDatabase.init_from_config_file('postgres.ini')
    db._connect()
    return db


def configure_websites():
    webs = open("websites.txt", "r")
    websites = webs.read().split('\n')
    webs.close()
    return websites


def convert_recursive(resolver):
    recursive = None
    if resolver == "1.1.1.1":
        recursive = "Cloudflare"
    elif resolver == "8.8.8.8":
        recursive = "Google"
    elif resolver == "9.9.9.9":
        recursive = "Quad9"
    return recursive


def convert_resolver(resolver):
    if resolver == "1.1.1.1":
        resolver = "https://cloudflare-dns.com/dns-query"
    elif resolver == "8.8.8.8":
        resolver = "https://dns.google/dns-qeury"
    elif resolver == "9.9.9.9":
        resolver = "https://dns.quad9.net/dns-query"
    return resolver


def configure_browsers():
    list = []
    while True:
        browser = input("Choose browser - Firefox / Chrome / Both: ").lower()
        if browser == "firefox":
            list.append("Firefox")
            break
        elif browser == "chrome":
            list.append("Chrome")
            break
        elif browser == "both":
            list.append("Firefox")
            list.append("Chrome")
            break
        else:
            print("Please try again!")
    return list


def container():
    database = configure_database()
    #resolver, operation_sys = configure_dns()
    resolver = "1.1.1.1"
    operation_sys = "Windows"
    recursive = convert_recursive(resolver)
    websites = configure_websites()
    browsers = configure_browsers()
    dns_type = ["dns", "dot", "doh"]
    delay = ping_resolver(resolver)
    return database, resolver, recursive, operation_sys, websites, browsers, dns_type, delay


def create_server():
    print("=====> Creating New Server - Please Wait... <=====")
    server = Server(browsermob_proxy_path)
    server.start()
    proxy = server.create_proxy()
    return proxy, server


def close_server(proxy, server):
    proxy.close()
    server.stop()


def main():
    proxy, server = create_server()
    configure_server(proxy)
    close_server(proxy, server)


if __name__ == "__main__":
    main()
