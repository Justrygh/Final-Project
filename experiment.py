import os


class Experiment:

    def __init__(self):
        self.browsers = []
        self.dns = []

    def select_browsers(self):
        """ Configure Browsers - Chrome / Firefox """
        while True:
            browser = input("Choose Browser - Firefox / Chrome / Both: ").lower()
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
        """ Configure DNS Types """
        counter = 0
        while counter != 1:
            output = input("Do you want to use Do53? (Y/N)").lower()
            if output == "y":
                self.dns.append("dns")
                counter += 1
            elif output == "n":
                counter += 1
            else:
                print("Wrong input, Please try again!")

        while counter != 2:
            output = input("Do you want to use DoT? (Y/N)").lower()
            if output == "y":
                self.dns.append("dot")
                counter += 1
            elif output == "n":
                counter += 1
            else:
                print("Wrong input, Please try again!")

        while counter != 3:
            output = input("Do you want to use DoH? (Y/N)").lower()
            if output == "y":
                self.dns.append("doh")
                counter += 1
            elif output == "n":
                counter += 1
            else:
                print("Wrong input, Please try again!")




