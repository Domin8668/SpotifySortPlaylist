from secrets import Data
from refresh import Refresh
import requests
from collections import namedtuple
from bisect import bisect_left
import json
import sys
import os


class SortSongs:
    def __init__(self):
        self.user_id: str = Data.spotify_user_id
        self.spotify_token: str = "AQBtJO9gXoZEew79eoecggYcrSabg4igWaF7VRDGVbF2YaK3piATbsvfDlS9Jf6imOAP0APrwA6OIeSwx" \
                                  "ypmOlGpFaYdZpD2wf_4hlpJRtM9zU4Zl0X-9rKyavDpLR7E5u4"
        self.playlist_id: str = Data.playlist_id
        self.snapshot_id: str = ''

        self.total: int = 0
        self.pivot: int = 1
        self.call_number: int = 0
        self.sort_number: int = 0

        self.tracks: list[namedtuple] = []

    def start(self) -> None:
        print("Refreshing token...")
        # Refreshing the authorization token.
        self.spotify_token = Refresh.refresh()
        # Getting the playlist snapshot
        self.get_playlist_snapshot_id()

    def get_playlist_snapshot_id(self):
        print("Getting the playlist's snapshot id...")
        # Getting the playlist data.
        query_params = "fields=snapshot_id,tracks.total"
        query = f'https://api.spotify.com/v1/playlists/{self.playlist_id}?{query_params}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self.spotify_token}'
        }
        response = requests.get(query, headers=headers)
        response_json = response.json()
        self.snapshot_id = response_json["snapshot_id"]
        self.total = response_json["tracks"]["total"]
        self.call_number = self.total // 50 + 1
        self.sort_number = self.total - self.pivot
        self.get_tracks()

    def get_tracks(self):
        print("Getting the tracks...")
        Track = namedtuple("Track", ["title", "artist", "album", "uri"])
        # Getting the tracks.
        for i in range(self.call_number):
            query_params = f'fields=items(track(name,uri,album(name,artists.name)))&offset={i * 50}&limit=50'
            # query_params = f'offset={i * 50}'
            query = f'https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks?{query_params}'
            headers = {
                "Content-Type": "application/json",
                "Authorization": f'Bearer {self.spotify_token}'
            }
            response = requests.get(query, headers=headers)
            response_json = response.json()
            for track in response_json["items"]:
                title = track["track"]["name"].casefold()
                artist = track["track"]["album"]["artists"][0]["name"].casefold()
                album = track["track"]["album"]["name"].casefold()
                uri = track["track"]["uri"]
                self.tracks.append(Track(title, artist, album, uri))
        self.insert_into_playlist()

    def insert_into_playlist(self):
        for _ in range(self.sort_number):
            to_sort = self.tracks.pop()
            idx = bisect_left(self.tracks, to_sort, lo=0, hi=self.pivot)
            sys.stdout.write("\rSorting: " + to_sort.title.ljust(20))
            sys.stdout.flush()
            self.tracks.insert(idx, to_sort)
            self.pivot += 1
            query = f'https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks'
            request_body = json.dumps({
                "range_start": self.total - 1,
                "insert_before": idx,
                "snapshot_id": self.snapshot_id
            })
            headers = {
                "Content-Type": "application/json",
                "Authorization": f'Bearer {self.spotify_token}'
            }
            response = requests.put(query, data=request_body, headers=headers)
            response_json = response.json()
            self.snapshot_id = response_json["snapshot_id"]
        os.system('cls||clear')
        sys.stdout.write("\rThe playlist is sorted!")
        sys.stdout.flush()


def main():
    s = SortSongs()
    s.start()


if __name__ == "__main__":
    main()
