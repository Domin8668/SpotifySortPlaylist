import base64


class Data:
    spotify_user_id = "domiins"
    playlist_ids = {"rap": "4IrYYzQPKEoYi1kLjpla63",
                    "gp": "1nePMthbW474oFv1VJTiI6",
                    "mood": "6FsVDArQUzUCTFg7vhfFd0",
                    "fav": "613aGyjw6qLa3VrLyn3yJu"}
    playlist_id = playlist_ids["mood"]

    refresh_token = "AQDZ-1GTXVOK3SoCCCnixwwdxS4aJyyy3N847u9nyOH9zW2Sts-nKMRGLQBiFlAG8yWH4HpYwqTBTLyHJcUahcYX2zbExf7" \
                    "JgmV-u-nJWt0zdeAcKte5V9myhXCDQOPESvk"
    redirect_uri = "https%3A%2F%2Fplaylist.srt"

    __client_secret = "cd3afad6cae9456abb3ba0c0c40e7c4a"
    __client_id = "0232f669246c47fd8ccb92da4fb428ff"
    client_creds_base64 = base64.b64encode(f'{__client_id}:{__client_secret}'.encode()).decode()
