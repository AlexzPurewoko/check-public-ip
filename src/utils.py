import ipaddress
import os
from git import Repo
from git.exc import InvalidGitRepositoryError

class Validator:
    def validateIp(ip):
        return ipaddress.ip_address(ip.strip()).__str__()

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
            (label, valueEntry) = line.split()
            self.__entries[label.strip()] = valueEntry.strip()
        file.close()
        

    def setEntry(self, key, value):
        self.__entries[key.strip()] = value.strip()

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
            commitMsg = 'Updating data :\n\n'
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
