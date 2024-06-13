import os
from utils import KeyEntryFileManager, GitManager, checkpublicip
import argparse
import netifaces


CONFIG_DIR = os.path.expanduser('~/.config/update-ip')
MAIN_CONFIG = CONFIG_DIR + '/config.txt'
IFACE_CONFIG = CONFIG_DIR + '/ifaces.txt'
REPO = CONFIG_DIR + '/repo'

def setupConfig():
    if os.path.exists(MAIN_CONFIG):
        return
    
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(MAIN_CONFIG, 'w+') as f:
        f.write(' ')
    
    os.chmod(MAIN_CONFIG, 0o600)

def loadConfig() -> KeyEntryFileManager:
    return KeyEntryFileManager(MAIN_CONFIG)

def reconfigure(entry):
    repository = input('Input your repository : ')
    entry.setEntry('repository', repository)
    entry.save()
    print('Configuration saved!')

def doUpdate(config):
    repo = config.getEntry('repository')
    gitmanager = GitManager(
        repo,
        REPO
    )
    gitmanager.open()

    entryIP = KeyEntryFileManager(REPO + '/ip_address.txt')

    for iface in netifaces.interfaces():
        if iface == 'lo':
            continue
        entryIP.setEntry(iface, checkpublicip(iface))

    entryIP.save()
    gitmanager.addFile('ip_address.txt')
    gitmanager.commit()
    gitmanager.publish()
    pass


setupConfig()
config = loadConfig()

parser = argparse.ArgumentParser(prog='update-ip')
parser.add_argument("-c", "--config", help="Configure the automatic update IP", action="store_true")

args = parser.parse_args()

if args.config:
    reconfigure(config)
else:
    if not config.keyExists('repository'):
        print('Configuration is gone or not existed yet. Please do configure first')
    else:
        doUpdate(config)
