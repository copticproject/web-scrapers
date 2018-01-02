import json
from lib.settings import Settings


class Output:
    def __init__(self):
        self.output_path = Settings.getOutputPath()
        self.script_info = Settings.getScriptInfo()

        self.rows = []

    def add(self, lang, title, link, link_to_file, site_specific_id, by, media_type):
        self.rows.append({
            'lang': lang,
            'title': title,
            'link': link,
            'link_to_file': link_to_file,
            'site_specific_id': site_specific_id,
            'by': by,
            'media_type': media_type
        })

    def write(self):
        with open(self.output_path, 'w', encoding='utf-8') as output_file:
            json.dump({
                'site': self.script_info['site'],
                'content_type': self.script_info['content_type'],
                'uploader': self.script_info['uploader'],
                'data': self.rows
            }, output_file, ensure_ascii=False)

