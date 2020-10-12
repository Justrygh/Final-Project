import os
from subprocess import run, check_output, STDOUT
from time import sleep


class Linux:

    def __init__(self):
        self.resolver = None
        self.recursive = None
        self.domain = None
        self.configure_dns()
        self.get_domain()

    def configure_doh_stub(self):
        listen_port = "53"
        listen_addr = "127.0.0.1"

        with open("../stubby_conf/resolv.conf", "w") as f:
            f.write("nameserver {0}".format(listen_addr))
        run(["sudo", "cp", "../stubby_conf/resolv.conf", "/etc/resolv.conf"])

        cmd = "sudo doh-stub --listen-port {0} --listen-address {1} --domain {2} --remote-address {3} > /dev/null " \
              "2>&1 &".format(listen_port, listen_addr, self.domain, self.resolver)
        os.system(cmd)

    def close_doh(self):
        with open("../stubby_conf/resolv.conf", "w") as f:
            f.write("nameserver " + self.resolver)
        run(["sudo", "cp", "../stubby_conf/resolv.conf", "/etc/resolv.conf"])
        os.system("pkill -9 doh-stub")

    def configure_stubby(self):
        """ Configure Stub Resolver - Stubby """
        with open("../stubby_conf/resolv.conf", "w") as f:
            f.write("nameserver 127.0.0.1")

        if self.resolver == '1.1.1.1':
            run(["sudo", "stubby", "-C", "../stubby_conf/stubby-cf.yml", "-g"])
        elif self.resolver == '9.9.9.9':
            run(["sudo", "stubby", "-C", "../stubby_conf/stubby-quad9.yml", "-g"])
        elif self.resolver == '8.8.8.8':
            run(["sudo", "stubby", "-C", "../stubby_conf/stubby-google.yml", "-g"])
        run(["sudo", "cp", "../stubby_conf/resolv.conf", "/etc/resolv.conf"])

    def close_stubby(self):
        """ Configure Stub Resolver - Stubby (= Default ) """
        with open("../stubby_conf/resolv.conf", "w") as f:
            f.write("nameserver " + self.resolver)
        run(["sudo", "cp", "../stubby_conf/resolv.conf", "/etc/resolv.conf"])
        os.system("pkill -9 stubby")

    def configure_resolver(self):
        """ Configure DNS Resolver - Cloudflare / Google / Quad9 """
        print("Make sure you run the script as administrator, if not please relaunch as administrator.")
        self.resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        while self.resolver != "1.1.1.1" and self.resolver != "8.8.8.8" and self.resolver != "9.9.9.9":
            print("Wrong input, Please try again!")
            self.resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        os.system('echo "nameserver {}" > /etc/resolv.conf'.format(self.resolver))

    def configure_recursive(self):
        """ Recursive - Name of the Resolver """
        if self.resolver == "1.1.1.1":
            self.recursive = "Cloudflare"
        elif self.resolver == "8.8.8.8":
            self.recursive = "Google"
        elif self.resolver == "9.9.9.9":
            self.recursive = "Quad9"

    def configure_dns(self):
        self.configure_resolver()
        self.configure_recursive()

    def get_dns_metadata(self):
        return self.resolver, self.recursive

    def tostring(self):
        return "Linux"

    def measure(self, dns_type, resolver, domains_filename):
        domains = "dns-timing/" + domains_filename
        cmd = ["dns-timing/dns-timing", dns_type, resolver, domains]
        output = check_output(cmd, stderr=STDOUT)
        output = output.decode('utf-8')
        return output

    def get_domain(self):
        """ Resolver for DoH - convert ip to address """
        if self.resolver == "1.1.1.1":
            self.domain = "cloudflare-dns.com"
        elif self.resolver == "8.8.8.8":
            self.domain = "dns.google"
        elif self.resolver == "9.9.9.9":
            self.domain = "dns.quad9.net"

