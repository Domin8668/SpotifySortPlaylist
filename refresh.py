from secrets import Data
import requests


class Refresh:
    def __init__(self):
        self.refresh_token = Data.refresh_token
        self.client_creds_base64 = Data.client_creds_base64

    @staticmethod
    def refresh():
        # Creating a POST request to the api to get a new token.
        query = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": Data.refresh_token
        }
        headers = {
            "Authorization": f'Basic {Data.client_creds_base64}',
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.post(query, data=data, headers=headers)

        return response.json()["access_token"]
