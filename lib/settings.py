import json
from lib.utilities import getFullPath

class Settings:
    __settings = json.load(open(getFullPath('settings.json')))

    @staticmethod
    def getYouTubeAppKey():
        return Settings.__settings['youtube-app-key']