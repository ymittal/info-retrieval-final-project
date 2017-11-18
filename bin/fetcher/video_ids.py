import os

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                                     SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def playlist_items_list_by_playlist_id(client, **kwargs):
    response = client.playlistItems().list(**kwargs).execute()
    if not response.get('items'):
        return [], None

    videoIds = []
    for item in response['items']:
        videoIds.append(str(item['contentDetails']['videoId']))
    if response.get('nextPageToken'):
        return videoIds, response['nextPageToken']
    else:
        return videoIds, None


def fetch_playlist_items(client, playlistId):
	"""Refer to the following SO answer for how to retrieve a list
	of uploaded video Ids for a given channel
	:see https://stackoverflow.com/a/13504900/4103546
	"""
    results = []
    nextPageToken = None
    while True:
        kwargs = {
            'part': 'contentDetails',
            'maxResults': 50,
            'playlistId': 'UUAuUUnT6oDeKwE6v1NGQxug'
        }
        if nextPageToken:
            kwargs['pageToken'] = nextPageToken
        videoIds, nextPageToken = playlist_items_list_by_playlist_id(client,
                                                                     **kwargs)
        results.extend(videoIds)
        if __debug__:
            print("no. of videos: %s, next page token: %s"
                  % (len(videoIds), nextPageToken))
        if not nextPageToken:
            break
    return results


def main():
    service = get_authenticated_service()
    # following playlist Id is for TEDtalksDirector's uploaded videos
    videoIds = fetch_playlist_items(service,
                                    playlistId='UUAuUUnT6oDeKwE6v1NGQxug')
    with open('uploaded_videos.txt', 'w') as fout:
        fout.write('\n'.join(videoIds))

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    main()
