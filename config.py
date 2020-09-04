from database import DNSDatabase


class Config:

    def __init__(self):
        self.database = None
        self.websites = None
        self.configuration()

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

    def configuration(self):
        self.configure_database()
        self.collect_websites()

    def get_websites(self):
        return self.websites

    def get_database(self):
        return self.database
