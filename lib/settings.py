import os
import sys
import json


# Calculate the root path of the project
root_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# Get the full path to the calling script and extract information
calling_script_path, calling_script_name = os.path.split(os.path.realpath(sys.argv[0]))
script_name, extension = os.path.splitext(calling_script_name)
calling_script_path, content_type = os.path.split(calling_script_path)
calling_script_path, upload_site = os.path.split(calling_script_path)
calling_script_path, uploader = os.path.split(calling_script_path)


class Settings:
    __settings = json.load(open(os.path.realpath(os.path.join(root_path, 'settings.json'))))


    @staticmethod
    def getYouTubeAppKey():
        return Settings.__settings['youtube-app-key']


    # Gets a path to a file relative to the project root folder
    @staticmethod
    def getFullPath(path):
        if os.path.isabs(path):
            return path
        else:
            return os.path.realpath(os.path.join(root_path, path))


    # Gets script information from path
    @staticmethod
    def getScriptInfo():
        return {
            'uploader': uploader,
            'site': upload_site,
            'content_type': content_type,
            'script_name': script_name
        }


    # Create path if not exist recursively
    @staticmethod
    def createPathRecursively(path):
        os.makedirs(path, exist_ok=True)


    # Get output path, and create the directory if not existing
    @staticmethod
    def getOutputPath():
        output_path = Settings.getFullPath(Settings.__settings['output-path'])
        script_info = Settings.getScriptInfo()

        output_path = os.path.join(output_path, script_info['uploader'])
        output_path = os.path.join(output_path, script_info['site'])
        output_path = os.path.join(output_path, script_info['content_type'])
        Settings.createPathRecursively(output_path)

        return os.path.join(output_path, script_info['script_name'] + '.json')