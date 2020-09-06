from database import DNSDatabase


class Config:

    def __init__(self):
        self.database = None
        self.websites = None
        self.config()

    def configure_database(self):
        print("=====> Connecting to Database - Please Wait... <=====")
        self.database = DNSDatabase.init_from_config_file('postgres.ini')
        self.database._connect()

    def collect_websites(self):
        print("=====> Collecting Websites - Please Wait... <=====")
        webs = open("websites.txt", "r")
        self.websites = webs.read().split('\n')
        if self.websites[-1] == '':
            del self.websites[-1]
        webs.close()

    def config(self):
        self.configure_database()
        self.collect_websites()

    def get_configuration(self):
        return self.database, self.websites
