from selenium import webdriver
import urllib.parse as urlparse
from database import DNSDatabase
import os
from proxy import Proxy as prox


class Config:

    def __init__(self):
        self.database = None
        self.websites = None

    def configure_database(self):
        """ Configure Database - PostgreSQL """
        self.database = DNSDatabase.init_from_config_file('postgres.ini')
        self.database._connect()

    def collect_websites(self):
        """ Configure Websites """
        webs = open("websites.txt", "r")
        self.websites = webs.read().split('\n')
        if self.websites[-1] == '':
            del self.websites[-1]
        webs.close()
