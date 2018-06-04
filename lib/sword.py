## Code ported from the PySword project on GitHub
import configparser
import json
import re
import struct
import sys
import os
import zlib


########################################################################################################
## Handling verse text source types
########################################################################################################
class OSISCleaner:
    __keep_tags = ['p', 'l', 'lg', 'q', 'a', 'w', 'divineName', 'foreign', 'hi', 'inscription',
                     'mentioned', 'name', 'reference', 'seg', 'transChange', 'salute', 'signed', 'verse',
                     'closer', 'speech', 'speaker', 'list', 'item', 'table', 'head', 'row', 'cell',
                     'caption', 'chapter', 'div']

    __remove_content_regexes = [re.compile(regex, re.IGNORECASE) for tag in
        ['note', 'milestone', 'title', 'abb', 'catchWord', 'index', 'rdg',
                                   'rdgGroup', 'figure'] for regex in
                            [f'<{tag}.*?{tag}>', f'<{tag}[^<]*/>']] + [
        re.compile(regex, re.IGNORECASE) for tag in __keep_tags for regex in [f'<{tag}[^<]*/>', f'</\s*{tag}>']]

    __keep_content_regexes = [re.compile(f'<{tag}.*?>(.*?)</{tag}>', re.IGNORECASE) for tag in __keep_tags]

    def clean(self, text):
        text = re.sub(r'(<[^\>]+type="x-br"[^\>]+\>)', r'\1 ', text)
        for regex in self.__keep_content_regexes:
            text = regex.sub(r'\1', text)
        for regex in self.__remove_content_regexes:
            text = regex.sub('', text)
        return text

class GBFCleaner:
    __remove_content_regexes = [re.compile(regex) for regex in [
        '<TB>.*?<Tb>', '<TC>.*?<Tc>', '<TH>.*?<Th>', '<TS>.*?<Ts>', '<TT>.*?<Tt>',
        '<TN>.*?<Tn>', '<TA>.*?<Ta>', '<TP>.*?<Tp>',
        '<FB>.*?<fb>', '<FC>.*?<fc>', '<FI>.*?<fi>', '<FN.*?>.*?<fn>', '<FO>.*?<fo>',
        '<FR>.*?<fr>', '<FS>.*?<fs>', '<FU>.*?<fu>', '<FV>.*?<fv>',
        '<RF>.*?<Rf>', '<RB>', '<RP.*?>', '<Rp.*?>', '<RX.*?>', '<Rx.*?>',
        '<H.*?>', '<B.*?>', '<ZZ>', '<D.*?>', '<J.*?>', '<P.>', '<W.*?>',
        '<S.*?>', '<N.*?>', '<C.>']]

    def clean(self, text):
        for regex in self.__remove_content_regexes:
            text = regex.sub('', text)
        # TODO: Support special char tags <CAxx> and <CUxxxx>
        return text


class ThMLCleaner:
    __remove_content_regexes = [re.compile(regex) for regex in [
        r'<scripRef.*?>.*?</scripRef>', r'<scripCom.*?>.*?</scripCom>', r'<.*?>']]

    def clean(self, text):
        for regex in self.__remove_content_regexes:
            text = regex.sub('', text)
        return text

########################################################################################################
## Handles calculations for a version of Bible books versification
########################################################################################################
class BooksVersificaton:
    with open('sword-versification.json') as file:
        __versificaton_dict = json.load(file)

    def __init__(self, versification):
        self.__versification = self.__versificaton_dict[versification]
        self.__calculate_books_info()

    def __calculate_books_info(self):
        if 'books_dict' not in self.__versification:
            self.__versification['books_dict'] = {}
            for testament in ['ot', 'nt']:
                book_offset = 2 # Bypass testament heading
                for book in self.__versification[testament]:
                    book['size'] = sum(book['chapters']) + len(book['chapters']) + 1
                    book['offset'] = book_offset
                    book_offset += book['size']

                    self.__versification['books_dict'][book['name']] = \
                        self.__versification['books_dict'][book['osis']] =\
                            (testament, book)
                    if book['abbr'] != book['osis']:
                        self.__versification['books_dict'][book['abbr']] = \
                            self.__versification['books_dict'][book['osis']]

    def get_verse_index(self, book_name, chapter_num, verse_number):
        book_info = self.__versification['books_dict'][book_name][1]
        index = book_info['offset'] + 1 # To the first chapter in the book skipping book title
        index += sum(book_info['chapters'][:chapter_num - 1]) + chapter_num # To the chapter skipping titles of previous chapters
        index += verse_number - 1# To the verse (skipping the chapter title)
        return index

    def get_book_testament(self, book_name):
        return self.__versification['books_dict'][book_name][0]

    def get_book_names(self, include_old_testament=True, include_new_testament=True):
        return [book['name'] for book in self.__versification['ot']] if include_old_testament else [] + \
               [book['name'] for book in self.__versification['nt']] if include_new_testament else []

    def get_book_chapters_verses(self, book_name):
        return self.__versification['books_dict'][book_name][1]['chapters']


########################################################################################################
## Represents Bible Module
########################################################################################################
class Bible:
    def __init__(self, module):
        self.__versification = BooksVersificaton(module.versification)
        self.__testaments = module.get_data_files()

    def get_all_verses(self):
        return {
            'ot': {
                book_name: self.get_book_verses(book_name)
                for book_name in self.__versification.get_book_names(include_new_testament=False)
            },
            'nt': {
                book_name: self.get_book_verses(book_name)
                for book_name in self.__versification.get_book_names(include_old_testament=False)
            }
        }

    def get_book_verses(self, book):
        data = self.__testaments[self.__versification.get_book_testament(book)]
        index = self.__versification.get_verse_index(book, 1, 1)
        verses = []
        for verses_count in self.__versification.get_book_chapters_verses(book):
            verses.append([data.read(index + i) for i in range(0, verses_count)])
            index += 1 + verses_count
        return verses

    def get_chapter_verses(self, book, chapter_num):
        data = self.__testaments[self.__versification.get_book_testament(book)]
        verses = range(1, self.__versification.get_book_chapters_verses(book)[chapter_num - 1] + 1)
        return [data.read(self.__versification.get_verse_index(book, chapter_num, v)) for v in verses]

    def get_verse(self, book, chapter_num, verse_num):
        data = self.__testaments[self.__versification.get_book_testament(book)]
        return data.read(self.__versification.get_verse_index(book, chapter_num, verse_num))


########################################################################################################
## Reads and seeks a SWORD modules file for verses
########################################################################################################
class ModuleDataFile:
    __record_formats = {
        'rawtext': {
            'format': '<IH',
            'compressed': False,
            'extensions': ['vss', '']
        },
        'rawtext4': {
            'format': '<II',
            'compressed': False,
            'extensions': ['vss', '']
        },
        'ztext': {
            'format': '<IIH',
            'compressed': True,
            'extensions': ['bzv', 'bzs', 'bzz']
        },
        'ztext4': {
            'format': '<III',
            'compressed': True,
            'extensions': ['bzv', 'bzs', 'bzz']
        }
    }

    def __init__(self, data_path, name, sourcetype):
        format_info = self.__record_formats[sourcetype]

        files = [os.path.join(data_path, f'{name}.{ext}')
                 for ext in format_info['extensions']]

        self.__text_file_handle = open(files[-1], 'rb')

        self.__indices = [self.__read_indices(files[0], format_info['format'])]
        if format_info['compressed']:
            self.__indices.append(self.__read_indices(files[1], '<III'))

    def __del__(self):
        self.__text_file_handle.close()

    @staticmethod
    def __read_indices(filename, format):
        indices = []

        with open(filename, "rb") as f:
            while True:
                data = f.read(struct.calcsize(format))
                if not data: break
                s = struct.unpack(format, data)
                indices.append(s)

        return indices

    @staticmethod
    def __decode(data, encoding=None):
        if not encoding:
            encoding = 'utf-8'
        return data.decode(encoding, 'strict')

    def read(self, index):
        if len(self.__indices) > 1:
            return self.__read_compressed(index)
        else:
            return self.__read_raw(index)

    def __read_raw(self, index):
        verse_start, verse_len = self.__indices[0][index]
        self.__text_file_handle.seek(verse_start)
        return self.__decode(self.__text_file_handle.read(verse_len))

    def __read_compressed(self, index):
        buf_num, verse_start, verse_len = self.__indices[0][index]
        offset, size, uc_size = self.__indices[1][buf_num]
        self.__text_file_handle.seek(offset)
        compressed_data = self.__text_file_handle.read(size)
        text = zlib.decompress(compressed_data)
        return self.__decode(text[verse_start:verse_start + verse_len])

    @staticmethod
    def load_all_files(data_path, moddrv):
        indices_ext = ModuleDataFile.__record_formats[moddrv]['extensions'][0]
        files = {}

        for file in os.listdir(data_path):
            if file.endswith(f'.{indices_ext}'):
                name = os.path.splitext(file)[0]
                files[name] = ModuleDataFile(data_path, name, moddrv)

        return files


########################################################################################################
## Represents a SWORD module
########################################################################################################
class Module:
    def __init__(self, installation_path, config_file):
        self.__installation_path = installation_path
        config = configparser.ConfigParser(strict=False)

        with open(config_file, mode='rt', encoding='utf-8', errors='strict') as conf_file:
            config.read_file(conf_file)

        self.__name = config.sections()[0]
        self.__fields = dict(config._sections[self.__name])

    def get_data_files(self):
        return ModuleDataFile.load_all_files(self.path, self.moddrv)

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return os.path.join(self.__installation_path, self.__fields['datapath'])

    @property
    def moddrv(self):
        return self.__fields['moddrv'].lower()

    @property
    def versification(self):
        return self.__fields['versification'].lower() if 'versification' in self.__fields else 'kjv'

    @property
    def encoding(self):
        return self.__fields['encoding'].lower() if 'encoding' in self.__fields else None

    @property
    def sourcetype(self):
        return self.__fields['sourcetype'].lower() if 'sourcetype' in self.__fields else None


########################################################################################################
## Represents a SWORD installation
########################################################################################################
class Sword:
    def __init__(self, installation_path=None):
        if installation_path is None:
            if sys.platform.startswith('win32'):
                installation_path = os.path.join(os.getenv('APPDATA'), 'Sword')
            elif sys.platform.startswith('darwin'):
                installation_path = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', 'Sword')
            else:  # Linux etc.
                installation_path = os.path.join(os.getenv('HOME'), '.sword')

        self.__installation_path = installation_path

    def get_all_modules(self):
        modules = {}

        config_path = os.path.join(self.__installation_path, 'mods.d')

        for file in os.listdir(config_path):
            if file.endswith('.conf'):
                module = Module(self.__installation_path, os.path.join(config_path, file))
                modules[module.name] = module

        return modules



##### Example code
# sword = Sword()
# modules = sword.get_all_modules()
# cleaner = OSISCleaner()
#
# ukjv = Bible(modules['AraSVD'])
# all = ukjv.get_all_verses()
#
# x = 1
# for c in all['ot']['Exodus']:
#     print(f'\nChapter {x}')
#     x += 1
#     n = 1
#     for v in c:
#         print(f'{n}: {cleaner.clean(v)}')
#         n += 1