import re
from lib.youtube import YouTube
from lib.output import Output

youtube = YouTube.instance

def getPlaylists():
    result = []

    playlists = youtube.playlists().list(part="id,snippet", channelId="UCDtJ-htmkHTQRAjFPb6GDbQ", maxResults=50).execute()

    while True:
        for item in playlists['items']:
            if -1 != item['snippet']['title'].find('البابا شنودة'):
                result.append({'id': item['id'],
                               'title': item['snippet']['title']})

        if 'nextPageToken' not in playlists:
            break

        playlists = youtube.playlists().list(pageToken=playlists['nextPageToken'],
                                             part="id,snippet", channelId="UCDtJ-htmkHTQRAjFPb6GDbQ", maxResults=50).execute()

    return result


def getVideos(playlistId):
    videos = []

    items = youtube.playlistItems().list(part="id,snippet", playlistId=playlistId, maxResults=50).execute()

    while True:
        for item in items['items']:
            videos.append({'id': item['id'],
                           'title': item['snippet']['title']})

        if 'nextPageToken' not in items:
            break

        items = youtube.playlistItems().list(pageToken=items['nextPageToken'],
                                             part="id,snippet", playlistId=playlistId, maxResults=50).execute()

    return videos


def extractInfoFromTitle(title):
    match = re.match(r'(?:\d+.\s+)?' +
                     r'(?P<title>.+)[ _-]+' +
                     r'(?P<day>\d+)[ -]+(?P<month>\d+)[ -]+(?P<year>\d+)[ _-]+' +
                     r'(?:(?P<venue>.+)[ _]+البابا|' +
                     r'البابا شنودة\s?الثالث[ _]+(?P<venue_end>.+))',
                     title)

    if match:
        print(match.group('title'))
    # if not match:
        # print('%s - %s/%s/%s - %s' % (match.group('title'), match.group('day'), match.group('month'), match.group('year'), match.group('venue')))
    # else:
    #     print(title)


output = Output()

for playlist in getPlaylists():
    for video in getVideos(playlist['id']):
        extractInfoFromTitle(video['title'])
        output.add('ar', video['title'], '', '', video['id'], 'البابا شنودة', 'Video')
        # exit(0)
        # es.index(index='scraps', doc_type='blob', body={
        #     'source': {'party': 'Coptic Treasure', 'app': 'Youtube'},
        #     'type': {'mediaType': 'video', 'blobType': 'sermon'},
        #     'person': 'Pope Shenouda III',
        #     # date, series, venue
        #     'youtubePlaylistId': playlist['id'],
        #     'youtubePlaylistTitle': playlist['title'],
        #     'youtubeId': video['id'],
        #     'title': video['title']
        # })

output.write()