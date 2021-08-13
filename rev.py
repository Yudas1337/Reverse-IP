#!/usr/bin/python
import os
import sys
import time
import json
import requests
import base64
import socket
import operator
from pathlib import Path
import pathlib
from optparse import OptionParser

# Reverse Ip CODED BY ./Exorcism1337
# YOU MUST REGISTER AN ACCOUNT IN viewdns.info OR THIS TOOLS WILL NOT WORKING!
# check your registered account API on viewdns.info


class Exorcism1337:

    black_list = ['http://', 'www.', "https://"]
    required = ['list']
    required_version = (3, 0)
    red = "\033[1;31;40m"
    green = "\033[1;32;40m"
    api_key = "YOUR_API_KEY"
    api_viewdns = "https://api.viewdns.info/reverseip/"
    api_hackertarget = "https://api.hackertarget.com/reverseiplookup/?q="
    usage = "Usage: python3 mager.py -l list.txt"
    version = "Reverse IP 1.0.2" + \
        " Coded By Python " + str(sys.version_info[0])
    parser = OptionParser(usage=usage, version=version)

    def __init__(self):
        self.author()
        self.params()

    def params(self):
        self.parser.add_option("-l", "--list", dest="list", type="string",
                               help="list.txt")
        (options, args) = self.parser.parse_args()
        try:
            for r in self.required:
                if options.__dict__[r] is None:
                    self.parser.error(
                        "parameter %s is required! see the usage with --help or -h" % r)
            if options.list:
                self.check_installation(self.required_version)
                self.checkSiteUri(options.list)

        except KeyboardInterrupt:
            print("Program Terminated")
            sys.exit(0)

    def check_installation(self, version):
        current_version = sys.version_info
        if current_version[0] == version[0] and current_version[1] >= version[1]:
            pass
        else:
            sys.stderr.write("[%s] - Error: Your Python interpreter must be %d.%d or greater (within major version %d)\n" %
                             (sys.argv[0], version[0], version[1], version[0]))
            sys.exit(-1)
        return 0

    def author(self):

        print("""\n██████╗ ███████╗██╗   ██╗███████╗██████╗ ███████╗███████╗    ██╗██████╗
██╔══██╗██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝    ██║██╔══██╗
██████╔╝█████╗  ██║   ██║█████╗  ██████╔╝███████╗█████╗      ██║██████╔╝
██╔══██╗██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝      ██║██╔═══╝
██║  ██║███████╗ ╚████╔╝ ███████╗██║  ██║███████║███████╗    ██║██║
╚═╝  ╚═╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝╚═╝
                                                                        """)
        print("""
            Author   : ./Exorcism1337
	    Contact  : c4tchMe1fY0uC4n@hackermail.com
	    Facebook : https://www.facebook.com/Yudas1337
	    Github   : https://github.com/Yudas1337
	    Version  :  1.0.2  \n""")

        print("  Using Api Key : " + self.api_key)

    def getHostByName(self, domain):
        return socket.gethostbyname(domain)

    def checkSiteUri(self, domainList):
        print(f'\n\n{self.green}Scanning File {domainList} :', end=" ")
        time.sleep(5)
        if not os.path.isfile(domainList):
            print(f'{self.red}File not Found. Program Terminated')
            sys.exit(-1)
        print(f'{self.green}File Found. Scanning domains list...')
        time.sleep(5)
        with open(domainList, 'r', encoding='utf-8') as listFile:
            text = listFile.read()
        listFile = text.split('\n')
        for domains in listFile:
            for blackList in self.black_list:
                if operator.contains(domains, blackList):
                    print(
                        f'{self.red}Invalid Domains {domains} . Don`t Contains {blackList}. Fixing...')
                    time.sleep(5)
                    domains = domains.replace(blackList, "")
                    print(f'{self.green}Domains Fixed {domains}')

            self.reverse(domains)

    def checkSiteExist(self, domains, send):
        try:
            print(f'Reversing "{domains}" using ViewDNS Api \n')
            for domain in send['response']['domains']:
                site = domain['name']
                self.download(domains, site, "viewdns")
            self.runHackerTarget(domains)

        except KeyboardInterrupt:
            print("\n Program Terminated")

    def runHackerTarget(self, domains):
        print(f'Reversing "{domains}" using HackerTarget Api \n')
        ip_address = self.getHostByName(domains)
        r = requests.get(self.api_hackertarget+ip_address)
        if r.status_code == 200:
            res = r.text
            arr = res.split("\n")
            total = len(arr)
            print("total Site Reversed : " + str(total))
            for site in arr:
                self.download(domains, site, "hackertarget")

    def reverse(self, domains):
        params = {
            "host": domains,
            "apikey": self.api_key,
            "output": "json"
        }
        try:
            r = requests.get(self.api_viewdns, params)
            if r.status_code == 200:
                res = r.text
                send = json.loads(res)
                count = send['response']['domain_count']
                print("total Site Reversed : " + count)
                self.checkSiteExist(domains, send)
            else:
                print(
                    "  Networks Error? site error? api error? check it manually")
                sys.exit()
        except KeyboardInterrupt:
            print("\n Program Terminated By User")

    def download(self, baseUrl, domain, type):
        time.sleep(2)
        if type == "hackertarget":
            url = "hackertarget/"
        else:
            url = "viewdns/"

        if not os.path.isdir(type):
            os.mkdir(type)

        filename = url + baseUrl + '.txt'
        if not os.path.isfile(filename):
            Path(filename).touch()

        fp = open(filename, 'a+')
        fp.write(domain + "\n")
        fp.close()

        print(f'{self.green}{domain} Written Successfuly using API {type}')


if __name__ == "__main__":
    Exorcism1337()
