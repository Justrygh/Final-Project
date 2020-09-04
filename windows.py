import os
from subprocess import call, run, PIPE


class Windows:

    def __init__(self):
        self.resolver = None
        self.recursive = None

    def configure_stubby(self):
        """ Configure Stub Resolver - Stubby """
        with open("stubby/resolv.conf", "w") as f:
            f.write("nameserver 127.0.0.1")

        if self.resolver == '1.1.1.1':
            run("ubuntu", shell=True, stdout=PIPE, input="sudo stubby -C stubby/stubby-cf.yml -g", encoding='ascii')
        elif self.resolver == '9.9.9.9':
            run("ubuntu", shell=True, stdout=PIPE, input="sudo stubby -C stubby/stubby-quad9.yml -g", encoding='ascii')
        elif self.resolver == '8.8.8.8':
            run("ubuntu", shell=True, stdout=PIPE, input="sudo stubby -C stubby/stubby-google.yml -g", encoding='ascii')
        run("ubuntu", shell=True, stdout=PIPE, input="sudo cp stubby/resolv.conf /etc/resolv.conf", encoding='ascii')

    def configure_resolver(self):
        """ Configure DNS Resolver - Cloudflare / Google / Quad9 """
        print("Make sure you run PyCharm / Python IDE as administrator, if not please relaunch as administrator.\n")
        os.system("netsh interface show interface")
        interface = input("Choose your interface according to your adapter & connection: ")
        self.resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        while self.resolver != "1.1.1.1" or self.resolver != "8.8.8.8" or self.resolver != "9.9.9.9":
            print("Wrong input, Please try again!")
            self.resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        os.system('netsh interface ip set dns name="{0}" source="static" address="{1}"'.format(interface, self.resolver))
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
        run("ubuntu", shell=True, stdout=PIPE, input="sudo cp stubby/resolv.conf /etc/resolv.conf", encoding='ascii')