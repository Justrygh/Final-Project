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
import subprocess
from subprocess import call, run, PIPE


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
    instructor = open("instructor_linux.txt", 'r')
    print(instructor.read())
    resolver = input("Choose your resolver ip - Cloudflare - 1.1.1.1, Google - 8.8.8.8, Quad9 - 9.9.9.9: ")
    os.system('echo "nameserver {}" > /etc/resolv.conf'.format(resolver))
    return resolver


def container():
    """ Configuration Container"""
    resolver = configure_dns()
    browsers = ["Firefox"]
    return resolver, browsers


def close_stubby(resolver):
    """ Configure Stub Resolver - Stubby (= Default ) """
    with open("stubby/resolv.conf", "w") as f:
        f.write("nameserver " + resolver)
    run(["sudo", "cp", "stubby/resolv.conf", "/etc/resolv.conf"])
