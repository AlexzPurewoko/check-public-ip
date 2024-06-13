from io import BytesIO
import ipaddress
import os
from git import Repo
from git.exc import InvalidGitRepositoryError
import pycurl
import re

EXCLUDED_IFACES = [
    'lo',
    'veth.*',
    'br-.*',
    'docker.*',
    'virbr.*',
]

class Validator:
    def validateIp(ip):
        return ipaddress.ip_address(ip.strip()).__str__()

    def ifaceExcluded(ifacename) -> bool:
        for excluded in EXCLUDED_IFACES:
            if re.match(excluded, ifacename):
                return True
        return False

class KeyEntryFileManager:
    def __init__(self, filePath):
        if not os.path.exists(filePath):
            raise FileNotFoundError()
        if not os.path.isfile(filePath):
            raise Exception('{} is not a file'.format(filePath))
        self.__filePath = filePath
        self.__entries = {}
        self.__alreadyFirstOpen = False
        self.__readEntries()
    
    def getEntries(self):
        return self.__entries

    def __readEntries(self):
        file = open(self.__filePath, "r")
        self.__alreadyFirstOpen = True
        self.__entries = {}
        for line in file:
            line = line.strip().split()
            if len(line) == 0:
                continue
            
            label = line[0]
            try:
                self.__entries[label.strip()] = line[1]
            except:
                self.__entries[label.strip()] = None
        file.close()
        
    def keyExists(self, *keys):
        for key in keys:
            for dictKey in self.__entries.keys():
                if dictKey == key.strip():
                    return True
        return False
    
    def remove(self, key):
        if (self.keyExists(key)):
            del self.__entries[key.strip()]

    def setEntry(self, key, value):
        self.__entries[key.strip()] = value.strip()

    def getEntry(self, key):
        return self.__entries[key]

    def save(self):
        if not self.__alreadyFirstOpen:
            raise Exception('You did not open the file yet first time')
        file = open(self.__filePath, "w")
        resultstr = ''
        for key, value in self.__entries.items():
            resultstr += '{} \t{}\n'.format(key, value)
        file.write(resultstr)
        file.close()


class GitManager:
    def __init__(self, repoUrl, localPath):
        self.__repoUrl = repoUrl
        self.__localPath = localPath
        self.__openedRepo = None

    def open(self):
        if not os.path.exists(self.__localPath):
            self.__openedRepo = self.__clone()
            return

        if len(os.listdir(self.__localPath)) == 0:
            self.__openedRepo = self.__clone()
            return
        
        try:
            self.__openedRepo = self.__openExisting()
        except InvalidGitRepositoryError:
            raise Exception('The DIR is not empty and not a repository!')             

    def addFile(self, relativeFilePath):
        if self.__openedRepo is None:
            raise Exception('Repo is not opened yet')
        self.__openedRepo.index.add(relativeFilePath)

    def commit(self, message=None):
        if self.__openedRepo is None:
            raise Exception('Repo is not opened yet')
        
        diffs = self.__openedRepo.index.diff('HEAD')
        if len(diffs) == 0:
            print('No updates required')
            return
        
        commitMsg = message
        if commitMsg is None:
            commitMsg = 'Updating some data.\n\n'
            for diff in diffs:
                if diff.a_path != diff.b_path:
                    commitMsg += '- {} to {}\n'.format(diff.a_path, diff.b_path)
                else:
                    commitMsg += '- {}'.format(diff.a_path)
        
        self.__openedRepo.index.commit(commitMsg)

    def publish(self):
        if self.__openedRepo is None:
            raise Exception('Repo is not opened yet')
        
        self.__openedRepo.remote().push()

    # PRIVATE
    def __clone(self):
        return Repo.clone_from(
            self.__repoUrl,
            self.__localPath
        )
    def __openExisting(self):
        return Repo(
            self.__localPath
        )

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
