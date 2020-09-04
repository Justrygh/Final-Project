import os
from subprocess import run


class Linux:

    def __init__(self):
        self.resolver = None
        self.recursive = None

    def configure_stubby(self):
        """ Configure Stub Resolver - Stubby """
        with open("stubby/resolv.conf", "w") as f:
            f.write("nameserver 127.0.0.1")

        if self.resolver == '1.1.1.1':
            run(["sudo", "stubby", "-C", "stubby/stubby-cf.yml", "-g"])
        elif self.resolver == '9.9.9.9':
            run(["sudo", "stubby", "-C", "stubby/stubby-quad9.yml", "-g"])
        elif self.resolver == '8.8.8.8':
            run(["sudo", "stubby", "-C", "stubby/stubby-google.yml", "-g"])
        run(["sudo", "cp", "stubby/resolv.conf", "/etc/resolv.conf"])

    def configure_resolver(self):
        """ Configure DNS Resolver - Cloudflare / Google / Quad9 """
        print("Make sure you run the script as administrator, if not please relaunch as administrator.")
        self.resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        while self.resolver != "1.1.1.1" or self.resolver != "8.8.8.8" or self.resolver != "9.9.9.9":
            print("Wrong input, Please try again!")
            self.resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        os.system('echo "nameserver {}" > /etc/resolv.conf'.format(self.resolver))
        self.configure_recursive()

    def configure_recursive(self):
        """ Recursive - Name of the Resolver """
        if self.resolver == "1.1.1.1":
            self.recursive = "Cloudflare"
        elif self.resolver == "8.8.8.8":
            self.recursive = "Google"
        elif self.resolver == "9.9.9.9":
            self.recursive = "Quad9"

    def close_stubby(self):
        """ Configure Stub Resolver - Stubby (= Default ) """
        with open("stubby/resolv.conf", "w") as f:
            f.write("nameserver " + self.resolver)
        run(["sudo", "cp", "stubby/resolv.conf", "/etc/resolv.conf"])
