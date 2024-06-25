import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils import log

class SheetsFileManager:
    def __init__(self, conf={}) -> None:
        self.__hasProperConfig = self.__checkConfExistance(conf)
        if not self.__hasProperConfig:
            return

        creds, _ = google.auth.load_credentials_from_dict({
            'type' : 'service_account',
            'project_id' : conf['SHEETS_PROJECT_ID'],
            "client_email": conf['SHEETS_CLIENT_EMAIL'],
            "token_uri": conf['GOOGLEAPI_TOKEN_URI'],
            'private_key': conf['SHEETS_PRIVATE_KEY']
        })

        self.__entries = {}
        self.__rangeKeyValues = 'RAW!A2:B'
        self.__sheetsId = conf['SHEETS_FILE_ID']
        self.__sheetServices = build('sheets', 'v4', credentials=creds).spreadsheets()
        self.__readEntries()
        self.__haveUpdates = False

    @staticmethod
    def __checkConfExistance(conf):
        for key in ['SHEETS_PROJECT_ID', 'SHEETS_CLIENT_EMAIL', 'GOOGLEAPI_TOKEN_URI', 'SHEETS_PRIVATE_KEY', 'SHEETS_FILE_ID']:
            if key not in conf:
                log(f"Key {key} doesn't exist in configuration! Skipping update to sheets!")
                return False
            
        return True
        
    def __readEntries(self):
        entries = self.__sheetServices.values().get(
            spreadsheetId = self.__sheetsId,
            range=self.__rangeKeyValues
        ).execute().get('values', [])

        for entry in entries:
            self.__entries[entry[0]] = entry[1]

    # def keyExists(self, *keys):
    #     for 
    def getEntries(self):
        if not self.__hasProperConfig:
            return {}

        return self.__entries
    
    def setEntry(self, key, value):
        if not self.__hasProperConfig:
            return

        strippedValue = value.strip()
        if self.keyExists(key) and strippedValue == self.__entries[key]:
            return
        self.__entries[key] = strippedValue
        self.__haveUpdates = True

    def getEntry(self, key):
        if not self.__hasProperConfig:
            return None

        return self.__entries[key]
    
    def keyExists(self, *keys):
        for key in keys:
            for dictKey in self.__entries.keys():
                if dictKey == key.strip():
                    return True
        return False
    
    def remove(self, key):
        if not self.__hasProperConfig:
            return

        if (self.keyExists(key)):
            del self.__entries[key.strip()]

    def save(self):
        if not self.__hasProperConfig:
            return

        if self.__haveUpdates is False:
            return
        
        computedValues = list()
        for key, value in self.__entries.items():
            computedValues.append([key, value])

        computedBody = {
            "values" :computedValues
        }

        try:
            self.__sheetServices.values().update(
                spreadsheetId = self.__sheetsId,
                range=self.__rangeKeyValues,
                valueInputOption='USER_ENTERED',
                body=computedBody
            ).execute()
            log("Sheets data updated!")
        except HttpError as error:
            log('Could not save the result to google sheets due to Http Error -> ' + error)
        

        