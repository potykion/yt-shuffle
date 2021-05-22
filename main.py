import os
import random

from dotenv import load_dotenv
import google_auth_oauthlib.flow
import googleapiclient.discovery


def main():
    load_dotenv()
    youtube = setup_youtube()
    playlist_items = get_all_playlist_items(youtube)
    reorder_playlist_items(youtube, playlist_items)


def setup_youtube():
    # https://developers.google.com/youtube/v3/docs/playlistItems/update?apix=true
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        os.environ["CLIENT_SECRET_JSON"],
        ["https://www.googleapis.com/auth/youtube.force-ssl"]
    )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        "youtube",
        "v3",
        credentials=credentials
    )
    return youtube


def get_all_playlist_items(youtube):
    # https://www.youtube.com/playlist?list=PLdb8DVmvU9i5bGINNz10f-ga_bqD41O4q
    playlist_id = "PLdb8DVmvU9i5bGINNz10f-ga_bqD41O4q"

    playlist_items = []
    cursor = None
    limit = 50

    while True:
        # https://developers.google.com/youtube/v3/docs/playlistItems/list
        list_resp = (
            youtube.playlistItems()
                .list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=limit,
                pageToken=cursor
            )
                .execute()
        )

        new_items = list_resp["items"]
        playlist_items.extend(new_items)
        print(len(playlist_items))

        if len(new_items) < limit:
            break
        else:
            cursor = list_resp["nextPageToken"]

    return playlist_items


def reorder_playlist_items(youtube, playlist_items):
    random.shuffle(playlist_items)

    for index, playlist_item in enumerate(playlist_items):
        print(f"{index + 1} / {len(playlist_items)}")
        # https://developers.google.com/youtube/v3/docs/playlistItems/update
        update_resp = youtube.playlistItems().update(
            part="snippet",
            body={
                "id": playlist_item["id"],
                "snippet": {
                    "playlistId": playlist_item["snippet"]["playlistId"],
                    "position": random.randint(0, len(playlist_items) - 1),
                    "resourceId": playlist_item["snippet"]["resourceId"]
                }
            }
        ).execute()


if __name__ == '__main__':
    main()
