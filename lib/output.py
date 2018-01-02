import codecs
import csv

class Output:
    def __init__(self, uploader, site, content_type, media_type):
        self.media_type = media_type
        self.site = site
        self.uploader = uploader
        self.content_type = content_type
        self.rows = []

    def add(self, lang, title, link, link_to_file, site_specific_id, by):
        self.rows.append([lang, title, link, link_to_file, site_specific_id, by])

    def write(self):
        with codecs.open('eggs.csv', 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer .writerow(['media_type', self.media_type])
            writer .writerow(['site', self.site])
            writer .writerow(['content_type', self.content_type])
            writer .writerow(['uploader', self.uploader])

            writer .writerow([])

            writer .writerow(['lang', 'title', 'link', 'link_to_file', 'site_specific_id', 'by'])

            for row in self.rows:
                writer .writerow(row)


'''
    def write(self):
        with codecs.open('eggs.csv', 'w', 'utf-8') as csvfile:
            csvfile.write('media_type,%s\r\n' % self.media_type)
            csvfile.write('site,%s\r\n' % self.site)
            csvfile.write('content_type,%s\r\n' % self.content_type)
            csvfile.write('uploader,%s\r\n' % self.uploader)

            csvfile.write('\r\n')

            csvfile.write('lang,title,link,link_to_file,site_specific_id,by')

            for row in self.rows:
                csvfile.write('%s\r\n' % ','.join(row))
                '''