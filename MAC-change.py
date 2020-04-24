#!/usr/bin/env python3
import binascii
import optparse
import os
import re
import subprocess
import time


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change Mac's address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Enter MAC address if you want it ")
    parser.add_option("-l", "--loop", dest="loop_by_min", type="int", help="Enter mins to change mac every mins you entered it")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig " + interface + " down"], shell=True)
    subprocess.call(["ifconfig " + interface + " hw ether " + new_mac], shell=True)
    subprocess.call(["ifconfig " + interface + " up"], shell=True)


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    result_of_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if result_of_mac:
        return str(result_of_mac.group(0))
    else:
        print("[-] Please check your interface (" + interface + ")")


def generate_random_mac(new_mac):
    if not new_mac:
        random_MAC = []
        i = 0
        while i < 6:
            random_hex = binascii.b2a_hex(os.urandom(1))
            random_hex = str(random_hex).replace("b'", '').replace("'", '')
            decimal = int(random_hex, 16)
            if i == 0 and decimal % 2 == 1:
                decimal += 1
                random_hex = hex(decimal).replace('0x', '')
            if len(random_hex) == 1:
                random_hex = "0" + random_hex
            random_hex = str(random_hex) + "'"
            random_MAC.append(str(random_hex).replace("'", ':'))
            i += 1
        string_random_MAC = ''.join(random_MAC)
        mac = string_random_MAC[:-1]
    else:
        mac = new_mac
    return mac


options = get_arguments()

while True:

    mac = generate_random_mac(options.new_mac)

    current_mac = get_current_mac(options.interface)

    print("Current MAC = " + str(current_mac))

    change_mac(options.interface, mac)

    current_mac = get_current_mac(options.interface)

    print("[+] MAC Address Changed to " + str(current_mac))

#    subprocess.call(["ifconfig " + options.interface], shell=True)

    if options.loop_by_min:
        time.sleep(int(options.loop_by_min) * 60)
        continue
    else:
        break

