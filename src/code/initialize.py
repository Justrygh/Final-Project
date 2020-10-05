

class Initialize:

    def __init__(self):
        self.browsers = []
        self.dns = []
        self.select()

    def select_browsers(self):
        print("Please select which Browser you wish to use in the experiment: ")
        while True:
            browser = input("Firefox / Chrome / Both: ").lower()
            if browser == "firefox":
                self.browsers.append("Firefox")
                break
            elif browser == "chrome":
                self.browsers.append("Chrome")
                break
            elif browser == "both":
                self.browsers.append("Firefox")
                self.browsers.append("Chrome")
                break
            else:
                print("Wrong input, Please try again!")

    def select_dns(self):
        print("Please select DNS types you wish to use in the experiment: ")
        while True:
            output = input("Do you want to use Do53? (Y/N): ").lower()
            if output == "y":
                self.dns.append("dns")
                break
            elif output == "n":
                break
            else:
                print("Wrong input, Please try again!")

        while True:
            output = input("Do you want to use DoT? (Y/N): ").lower()
            if output == "y":
                self.dns.append("dot")
                break
            elif output == "n":
                break
            else:
                print("Wrong input, Please try again!")

        while True:
            output = input("Do you want to use DoH? (Y/N): ").lower()
            if output == "y":
                self.dns.append("doh")
                break
            elif output == "n":
                break
            else:
                print("Wrong input, Please try again!")

    def select(self):
        self.select_browsers()
        self.select_dns()

    def get_initialization(self):
        return self.browsers, self.dns



