from googleapiclient.discovery import build
from lib.settings import Settings

class YouTube:
    instance = build(serviceName="youtube", version="v3", developerKey = Settings.getYouTubeAppKey())
