import os
from utils import KeyEntryFileManager, GitManager, checkpublicip, Validator, log
from dotenv import dotenv_values
from sheetsutils import SheetsFileManager
import argparse
import netifaces



CONFIG_DIR = os.path.expanduser('~/.config/update-ip')
MAIN_CONFIG = CONFIG_DIR + '/config.txt'
ENV_CONFIG = CONFIG_DIR + '/.env'
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
    log('Configuration saved!')

def doUpdate(config, configEnv={}):
    log('Start Collecting Public IP for updates')
    repo = config.getEntry('repository')
    gitmanager = GitManager(
        repo,
        REPO
    )
    gitmanager.open()

    entryIP = KeyEntryFileManager(REPO + '/ip_address.txt')
    sheetsFileManager = SheetsFileManager(configEnv)

    for iface in netifaces.interfaces():
        if Validator.ifaceExcluded(iface):
            continue

        try:
            publicIp = checkpublicip(iface)
            entryIP.setEntry(iface, publicIp)
            sheetsFileManager.setEntry(iface, publicIp)
            log(f"Successfully collect IP from : {iface}")
        except:
            log(f"Failed to get IP on interface : {iface}")

    entryIP.save()
    gitmanager.addFile('ip_address.txt')
    gitmanager.commit()
    gitmanager.publish()
    sheetsFileManager.save()
    log('Program runned successfully. Exited now...')


setupConfig()
config = loadConfig()
configEnv = dotenv_values(ENV_CONFIG)

parser = argparse.ArgumentParser(prog='update-ip')
parser.add_argument("-c", "--config", help="Configure the automatic update IP", action="store_true")

args = parser.parse_args()

if args.config:
    reconfigure(config)
else:
    if not config.keyExists('repository'):
        log('Configuration is gone or not existed yet. Please do configure first')
    else:
        doUpdate(config)
