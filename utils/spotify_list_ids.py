def get_spotify_track_uris(sp, track_list, access_token) -> list[str]:
    spotify_uris = []

    for track in track_list:
        title = track.title
        artist = track.artist

        spotify_id = sp.search_track_in_spotify(title, artist, access_token)
        if spotify_id:
            spotify_uris.append(spotify_id)

    return spotify_uris
