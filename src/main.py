import argparse
import netifaces
from utils import Validator, checkpublicip

def showlistinterfaces():
    print("List your available Network interfaces: ")
    
    for iface in netifaces.interfaces():
        if Validator.ifaceExcluded(iface):
            continue
        print(iface)


parser = argparse.ArgumentParser(prog='check-public-ip')
parser.add_argument("-i", "--ifaces", type=str, help="String of network interfaces available on your devices")
parser.add_argument("-a", "--list-ifaces", help="Display available list network interfaces", action="store_true")
parser.add_argument("-t", "--timeout", type=int, default=10, help="Sets the timeout of program to check a public IP")

args = parser.parse_args()

if args.list_ifaces:
    showlistinterfaces()
else:
    print(checkpublicip(args.ifaces, args.timeout).strip(), end="")
