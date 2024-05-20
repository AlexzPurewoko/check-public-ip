import pycurl
from io import BytesIO
import argparse
import netifaces

# only get text value
def geturlfromiface(url, iface=None, timeout=10):
    curl = pycurl.Curl()
    dataBuffer = BytesIO()

    # set the options
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.TIMEOUT, timeout)
    curl.setopt(pycurl.WRITEFUNCTION, dataBuffer.write)

    if iface is not None:
        curl.setopt(pycurl.INTERFACE, iface)

    # perform the operation
    curl.perform()

    response = dataBuffer.getvalue().decode('UTF-8')
    dataBuffer.close()
    curl.close()

    return response


def checkpublicip(iface=None, timeout=10):
    return geturlfromiface("https://checkip.amazonaws.com", iface, timeout)

def showlistinterfaces():
    print("List your available Network interfaces: ")
    
    for iface in netifaces.interfaces():
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
