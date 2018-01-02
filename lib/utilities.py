import os

rootPath = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

def getFullPath(path):
    return os.path.realpath(os.path.join(rootPath, path))