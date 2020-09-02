import platform
import windows
import linux
import os


# def create_server():
#     """ Configure Server """
#     print("=====> Creating New Server - Please Wait... <=====")
#     server = Server(configure_proxy())
#     server.start()
#     proxy = server.create_proxy()
#     return proxy, server
#
#
# def chrome_browser(proxy):
#     """ Configure Chrome Web Driver for Windows """
#     chrome_driver = os.getcwd() + "chromedriver.exe"
#     url = urlparse.urlparse(proxy.proxy).path
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--proxy-server={0}".format(url))
#     chrome_options.add_argument('--ignore-certificate-errors')
#     driver = webdriver.Chrome(chrome_driver, options=chrome_options)
#     return driver
#
#
# def firefox_browser(proxy):
#     """ Configure Firefox Web Driver """
#     profile = webdriver.FirefoxProfile()
#     selenium_proxy = proxy.selenium_proxy()
#     profile.set_proxy(selenium_proxy)
#     driver = webdriver.Firefox(firefox_profile=profile)
#     return driver
#
#
# def ping_resolver(resolver_ip, count=5):
#     """ Send "count" pings """
#     delays = []
#     for i in range(count):
#         try:
#             d = ping(resolver_ip, unit='ms')
#             if d:
#                 delays.append(d)
#         except Exception as e:
#             print('ping error:', e)
#             return []
#     return delays
#
#
# def configure_database():
#     """ Configure Database - PostgreSQL """
#     db = DNSDatabase.init_from_config_file('postgres.ini')
#     db._connect()
#     return db
#
#
# def configure_websites():
#     """ Configure Websites """
#     webs = open("websites.txt", "r")
#     websites = webs.read().split('\n')
#     if websites[-1] == '':
#         del websites[-1]
#     webs.close()
#     return websites
#
#
# def convert_recursive(resolver):
#     """ Recursive - Name of the Resolver """
#     recursive = None
#     if resolver == "1.1.1.1":
#         recursive = "Cloudflare"
#     elif resolver == "8.8.8.8":
#         recursive = "Google"
#     elif resolver == "9.9.9.9":
#         recursive = "Quad9"
#     return recursive
#
#
# def convert_resolver(resolver):
#     """ Resolver for DoH - convert ip to url """
#     if resolver == "1.1.1.1":
#         resolver = "https://cloudflare-dns.com/dns-query"
#     elif resolver == "8.8.8.8":
#         resolver = "https://dns.google/dns-qeury"
#     elif resolver == "9.9.9.9":
#         resolver = "https://dns.quad9.net/dns-query"
#     return resolver
#
#
# def close_server(proxy, server):
#     """ Close the Server """
#     proxy.close()
#     server.stop()


########################################################################################################################
# def configure_proxy():
#     """ Configure Proxy Server (BrowserMob Proxy) """
#     browsermob_proxy_path = os.getcwd()  # path to firefox web driver
#     browsermob_proxy = ["browsermob-proxy-2.1.4", "bin", "browsermob-proxy"]
#     for path in browsermob_proxy:
#         browsermob_proxy_path = os.path.join(browsermob_proxy_path, path)
#     if platform.system() == "Windows":
#         browsermob_proxy_path += ".bat"
#     return browsermob_proxy_path


# def configure_stubby(resolver):
#     """ Configure Stub Resolver - Stubby """
#     operation_system = platform.system()
#     with open("stubby/resolv.conf", "w") as f:
#         f.write("nameserver 127.0.0.1")
#
#     if operation_system == "Linux":
#         if resolver == '1.1.1.1':
#             run(["sudo", "stubby", "-C", "stubby/stubby-cf.yml", "-g"])
#         elif resolver == '9.9.9.9':
#             run(["sudo", "stubby", "-C", "stubby/stubby-quad9.yml", "-g"])
#         elif resolver == '8.8.8.8':
#             run(["sudo", "stubby", "-C", "stubby/stubby-google.yml", "-g"])
#         run(["sudo", "cp", "stubby/resolv.conf", "/etc/resolv.conf"])
#
#     elif operation_system == "Windows":
#         if resolver == '1.1.1.1':
#             run("ubuntu", shell=True, stdout=PIPE, input="sudo stubby -C stubby/stubby-cf.yml -g", encoding='ascii')
#         elif resolver == '9.9.9.9':
#             run("ubuntu", shell=True, stdout=PIPE, input="sudo stubby -C stubby/stubby-quad9.yml -g", encoding='ascii')
#         elif resolver == '8.8.8.8':
#             run("ubuntu", shell=True, stdout=PIPE, input="sudo stubby -C stubby/stubby-google.yml -g", encoding='ascii')
#         run("ubuntu", shell=True, stdout=PIPE, input="sudo cp stubby/resolv.conf /etc/resolv.conf", encoding='ascii')


# def configure_dns():
#     """ Configure DNS Resolver - Cloudflare / Google / Quad9 """
#     resolver = None
#     operation_system = platform.system()
#     if operation_system == "Windows":
#         instructor = open("instructor_windows.txt", 'r')
#         print(instructor.read())
#         os.system("netsh interface show interface")
#         interface = input("Choose your interface according to your adapter & connection: ")
#         resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
#         os.system('netsh interface ip set dns name="{0}" source="static" address="{1}"'.format(interface, resolver))
#
#     elif operation_system == "Linux":
#         instructor = open("instructor_linux.txt", 'r')
#         print(instructor.read())
#         resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
#         os.system('echo "nameserver {}" > /etc/resolv.conf'.format(resolver))
#
#     elif operation_system == "Darwin":
#         instructor = open("instructor_mac.txt", 'r')
#         print(instructor.read())
#         os.system("networksetup listallnetworkservices")
#         interface = input("Choose your interface according to your adapter & connection: ")
#         resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
#         os.system("networksetup -setdnsservers {0} {1}".format(interface, resolver))
#     else:
#         print("Error: Our script supports Windows/Linux/Darwin(Mac) Operation Systems Only!")
#     return resolver
########################################################################################################################


# def configure_server(proxy):
#     """ The Experiment - HAR + DNS """
#     database, resolver, recursive, websites, browsers, dns_type, delay = container()
#     operation_system = platform.system()
#     for browser in browsers:
#         experiment = uuid.uuid1()
#         print("=====> Configuring Server - Please Wait... <=====")
#         if browser == "Chrome":
#             driver = chrome_browser(proxy)
#             print("=====> Using Google Chrome <=====")
#         if browser == "Firefox":
#             driver = firefox_browser(proxy)
#             print("=====> Using Firefox <=====")
#         for dns in dns_type:
#             if dns == "dot":
#                 configure_stubby(resolver)
#             for website in websites:
#                 har_uuid = uuid.uuid1()
#                 print("===========================================================")
#                 print("Type: ", dns, " | Resolver: ", recursive)
#                 print("Creating HAR for Website: https://{}".format(website))
#                 proxy.new_har("https://{}".format(website), options={'captureHeaders': True})
#                 driver.get("https://{}".format(website))
#                 har = json.loads(json.dumps(proxy.har))
#                 rv = database.insert_har(experiment, website, browser, recursive, operation_system, dns, har, har_uuid, None, delay)
#                 if not rv:
#                     print("Saved HAR for website {}".format(website))
#                 if dns == "doh":
#                     resolver = convert_resolver(resolver)
#                 try:
#                     dns_info = measure_dns(website, har, dns, resolver)
#                     if dns_info:
#                         rv_dns = database.insert_dns(har_uuid, experiment, browser, recursive, operation_system, dns, dns_info)
#                         if not rv_dns:
#                             print("Saved DNS for website {}".format(website))
#                             print("===========================================================\n")
#                     else:
#                         print("===========================================================\n")
#                 except:
#                     print("An exception occurred! Please try again later.")
#
#         if dns == "dot":
#             close_stubby(resolver)
#         driver.quit()


########################################################################################################################
# def configure_browsers():
#     """ Configure Browsers - Chrome / Firefox """
#     operation_system = platform.system()
#     if operation_system == "Windows" or operation_system == "Darwin":
#         while True:
#             browser = input("Choose browser - Firefox / Chrome / Both: ").lower()
#             if browser == "firefox":
#                 return ["Firefox"]
#             elif browser == "chrome":
#                 return ["Chrome"]
#             elif browser == "both":
#                 return ["Firefox", "Chrome"]
#             else:
#                 print("Please try again!")
#     else:
#         return ["Firefox"]
########################################################################################################################


# def container():
#     """ Configuration Container"""
#     database = configure_database()
#     #resolver = configure_dns()
#     resolver = "1.1.1.1"
#     recursive = convert_recursive(resolver)
#     websites = configure_websites()
#     browsers = configure_browsers()
#     dns_type = ["dns", "dot"]
#     delay = ping_resolver(resolver)
#     return database, resolver, recursive, websites, browsers, dns_type, delay


########################################################################################################################
# def close_stubby(resolver):
#     """ Configure Stub Resolver - Stubby (= Default ) """
#     operation_system = platform.system()
#     with open("stubby/resolv.conf", "w") as f:
#         f.write("nameserver " + resolver)
#     if operation_system == "Linux":
#         run(["sudo", "cp", "stubby/resolv.conf", "/etc/resolv.conf"])
#     elif operation_system == "Windows":
#         run("ubuntu", shell=True, stdout=PIPE, input="sudo cp stubby/resolv.conf /etc/resolv.conf", encoding='ascii')
#######################################################################################################################


def main():
    operation_system = platform.system()
    if operation_system == "Windows":
        #windows.start()
        print(os.getcwd())
    elif operation_system == "Linux":
        linux.start()
    else:
        print(" Windows / Linux Only!")


if __name__ == "__main__":
    main()
