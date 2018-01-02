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


output = Output()

for playlist in getPlaylists():
    for video in getVideos(playlist['id']):
        print(video['title'])
        output.add('ar', video['title'], '', '', video['id'], 'البابا شنودة', 'Video')
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