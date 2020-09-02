import os
from subprocess import run


def configure_stubby(resolver):
    """ Configure Stub Resolver - Stubby """
    with open("stubby/resolv.conf", "w") as f:
        f.write("nameserver 127.0.0.1")

    if resolver == '1.1.1.1':
        run(["sudo", "stubby", "-C", "stubby/stubby-cf.yml", "-g"])
    elif resolver == '9.9.9.9':
        run(["sudo", "stubby", "-C", "stubby/stubby-quad9.yml", "-g"])
    elif resolver == '8.8.8.8':
        run(["sudo", "stubby", "-C", "stubby/stubby-google.yml", "-g"])
    run(["sudo", "cp", "stubby/resolv.conf", "/etc/resolv.conf"])


def configure_dns():
    """ Configure DNS Resolver - Cloudflare / Google / Quad9 """
    print("Make sure you run the script as administrator, if not please relaunch as administrator.")
    resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
    os.system('echo "nameserver {}" > /etc/resolv.conf'.format(resolver))
    return resolver


def close_stubby(resolver):
    """ Configure Stub Resolver - Stubby (= Default ) """
    with open("stubby/resolv.conf", "w") as f:
        f.write("nameserver " + resolver)
    run(["sudo", "cp", "stubby/resolv.conf", "/etc/resolv.conf"])
