import json


class Output:
    def __init__(self, uploader, site, content_type, media_type):
        self.media_type = media_type
        self.site = site
        self.uploader = uploader
        self.content_type = content_type
        self.rows = []

    def add(self, lang, title, link, link_to_file, site_specific_id, by):
        self.rows.append({
            'lang': lang,
            'title': title,
            'link': link,
            'link_to_file': link_to_file,
            'site_specific_id': site_specific_id,
            'by': by})

    def write(self):
        with open('result.json', 'w', encoding='utf-8') as output_file:
            json.dump({
                'media_type': self.media_type,
                'site': self.site,
                'content_type': self.content_type,
                'uploader': self.uploader,
                'data': self.rows
            }, output_file, ensure_ascii=False)

