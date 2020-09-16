import os
from subprocess import run, PIPE


class Windows:

    def __init__(self):
        self.resolver = None
        self.recursive = None
        self.domain = None
        self.interface = None
        self.configure_dns()
        self.get_domain()

    def configure_stubby(self):
        """ Configure Stub Resolver - Stubby """
        listing_addr = "127.0.0.1"
        os.system('netsh interface ip set dns name="{0}" source="static" address="{1}"'.format(self.interface, listing_addr))

        if self.resolver == '1.1.1.1':
            os.system("..\Stubby\stubby.exe -C ..\stubby_conf\stubby-cf.yml")
        elif self.resolver == '9.9.9.9':
            os.system("..\Stubby\stubby.exe -C ..\stubby_conf\stubby-quad9.yml")
        elif self.resolver == '8.8.8.8':
            os.system("..\Stubby\stubby.exe -C ..\stubby_conf\stubby-google.yml")


    def close_stubby(self):
        """ Configure Stub Resolver - Stubby (= Default ) """
        print(self.interface + "   " + self.resolver)
        os.system('netsh interface ip set dns name="{0}" source="static" address="{1}"'.format(self.interface, self.resolver))
        os.system('taskkill /IM "stubby.exe" /F')


    def configure_resolver(self):
        """ Configure DNS Resolver - Cloudflare / Google / Quad9 """
        print("Make sure you run PyCharm / Python IDE as administrator, if not please relaunch as administrator.\n")
        os.system("netsh interface show interface")
        self.interface = 'wi-fi'                                                                                   #input("Choose your interface according to your adapter & connection: ")
        self.resolver =  "8.8.8.8"                                                                                 # input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        while self.resolver != "1.1.1.1" and self.resolver != "8.8.8.8" and self.resolver != "9.9.9.9":
            print("Wrong input, Please try again!")
            self.resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
        os.system('netsh interface ip set dns name="{0}" source="static" address="{1}"'.format(self.interface, self.resolver))

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

    @staticmethod
    def tostring():
        return "Windows"

    @staticmethod
    def measure(dns_type, resolver, domains_filename):
        cmd = "dns-timing/dns-timing {0} {1} {2}".format(dns_type, resolver, domains_filename)
        project_path = os.getcwd()
        project_path = project_path.split("\\")
        project_path[0] = project_path[0][:-1].lower()
        project_path = "/".join(project_path)
        project_path = "cd ../../mnt/" + project_path
        run_input = project_path + " && " + cmd
        output = run("ubuntu", shell=True, stdout=PIPE, input=run_input, encoding='ascii')
        return output

    def get_domain(self):
        """ Resolver for DoH - convert ip to address """
        if self.resolver == "1.1.1.1":
            self.domain = "cloudflare-dns.com"
        elif self.resolver == "8.8.8.8":
            self.domain = "dns.google"
        elif self.resolver == "9.9.9.9":
            self.domain = "dns.quad9.net"
