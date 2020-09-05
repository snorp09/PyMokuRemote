#!/bin/python

import ipaddress
import sys
import requests


class NotRoku(Exception):
    pass


try:
    ipaddress.ip_address(sys.argv[1])
except ValueError:
    print("Please include an ip address when calling the command.")
    exit(1)
except IndexError:
    print("Usage: remote [ip address]")
    exit(1)


def setip(ip):
    ip = "http://" + ip + ":8060"
    if requests.get(ip + '/query/device-info').status_code != 200:
        raise NotRoku
    return ip


try:
    roku = setip(sys.argv[1])
except NotRoku:
    print("Error! Not a roku.")

    send = None

while True:
    usrinput = input('Roku> ')
    if usrinput == 'help':
        print('Standard commands: "Up, Down, Left, Right, Home, Rev, Fwd, Play, Select, Backspace')
    elif usrinput == "exit":
        exit(0)
    elif usrinput == "roku":
        print(roku)
    elif "change" in usrinput:
        try:
            newip = usrinput.split(' ')[1]
            try:
                roku = setip(newip)
            except NotRoku:
                print("IP address isn't a roku.")
        except IndexError:
            print("change requires an IP address.")
    elif usrinput.isspace():
        print('Insert command or use help for a list of standard commands.')
    else:
        send = requests.post(roku + '/keypress/' + usrinput).status_code
        if send != 200:
            print("Not a roku command.")