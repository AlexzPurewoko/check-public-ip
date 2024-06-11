import ipaddress
import os

class IpUtilsManager:
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
            (label, ip) = line.split()
            self.__entries[label.strip()] = ip.strip()
        file.close()
        

    def setEntry(self, key, value):
        strippedIp = ipaddress.ip_address(value.strip()).__str__()
        self.__entries[key.strip()] = strippedIp

    def save(self):
        if not self.__alreadyFirstOpen:
            raise Exception('You did not open the file yet first time')
        file = open(self.__filePath, "w")
        resultstr = ''
        for key, value in self.__entries.items():
            resultstr += '{} \t{}\n'.format(key, value)
        file.write(resultstr)
        file.close()


