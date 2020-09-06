import uuid
import platform
from ping3 import ping
from dns_timings import measure_dns
from proxy import Proxy
from config import Config
from initialize import Initialize
from windows import Windows
from linux import Linux


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


def experiment(web_driver):
    """ Experiment """
    database, websites, browsers, dns_types, resolver, recursive, system, delay = container()
    proxy = web_driver.get_proxy()
    for browser in browsers:
        experiment_uuid = uuid.uuid1()
        print("=====> Configuring Server - Please Wait... <=====")
        if browser == "Chrome":
            web_driver.chrome_browser()
            driver = web_driver.get_driver()
            print("=====> Using Google Chrome <=====")
        if browser == "Firefox":
            web_driver.firefox_browser()
            driver = web_driver.get_driver()
            print("=====> Using Firefox <=====")
        for dns in dns_types:
            if dns == "dot":
                system.configure_stubby()
            for website in websites:
                har_uuid = uuid.uuid1()
                print("===========================================================")
                print("Type: ", dns, " | Resolver: ", recursive)
                print("Creating HAR for Website: https://{}".format(website))
                proxy.new_har("https://{}".format(website), options={'captureHeaders': True})
                driver.get("https://{}".format(website))
                har = proxy.har
                rv = database.insert_har(experiment_uuid, website, browser, recursive, system.tostring(), dns, har, har_uuid, None, delay)
                if not rv:
                    print("Saved HAR for website {}".format(website))
                try:
                    dns_info = measure_dns(website, har, dns, resolver, system)
                    if dns_info:
                        rv_dns = database.insert_dns(har_uuid, experiment_uuid, browser, recursive, system.tostring(), dns, dns_info)
                        if not rv_dns:
                            print("Saved DNS for website {}".format(website))
                            print("===========================================================\n")
                    else:
                        print("===========================================================\n")
                except:
                    print("An exception occurred! Please try again later.")

            if dns == "dot":
                system.close_stubby()
        driver.quit()


def container():
    c = Config()
    database, websites = c.get_configuration()

    i = Initialize()
    browsers, dns_types = i.get_initialization()

    operation_system = platform.system()
    if operation_system == "Windows":
        system = Windows()
    elif operation_system == "Linux":
        system = Linux()

    resolver, recursive = system.get_dns_metadata()
    delay = ping_resolver(resolver)

    return database, websites, browsers, dns_types, resolver, recursive, system, delay


def main():
    p = Proxy()
    p.create_server()
    experiment(p)


if __name__ == '__main__':
    main()
