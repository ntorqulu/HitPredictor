
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import numpy as np
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns


def data_scraping():
    credentials = json.load(open('Authorization.json'))
    # own client id and client secret on the Spotify developers account
    client_id = credentials['client_id']
    client_secret = credentials['client_secret']

    # number of the playlist we'll evaluate
    playlist_index = 0

    playlists = json.load(open('Playlists_like_dislike.json'))
    playlist_uri = playlists[playlist_index]['uri']
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    uri = playlist_uri  # the URI is split by ':' to get the username and playlist ID
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]

    results = sp.user_playlist_tracks(username, playlist_id)

    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    results = tracks
    playlist_tracks_id = []
    playlist_tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []
    playlist_tracks_first_release_date = []
    playlist_tracks_popularity = []

    for i in range(len(results)):
        print(i)  # counter
        if i == 0:
            playlist_tracks_id = results[i]['track']['id']
            playlist_tracks_titles = results[i]['track']['name']
            playlist_tracks_first_release_date = results[i]['track']['album']['release_date']
            playlist_tracks_popularity = results[i]['track']['popularity']

            artist_list = []
            for artist in results[i]['track']['artists']:
                artist_list = artist['name']
            playlist_tracks_artists = artist_list

            features = sp.audio_features(playlist_tracks_id)
            features_df = pd.DataFrame(data=features, columns=features[0].keys())
            features_df['title'] = playlist_tracks_titles
            features_df['all_artists'] = playlist_tracks_artists
            features_df['popularity'] = playlist_tracks_popularity
            features_df['release_date'] = playlist_tracks_first_release_date
            features_df = features_df[['id', 'title', 'all_artists', 'popularity', 'release_date',
                                       'danceability', 'energy', 'key', 'loudness',
                                       'mode', 'acousticness', 'instrumentalness',
                                       'liveness', 'valence', 'tempo',
                                       'duration_ms', 'time_signature']]
            continue
        else:
            try:
                playlist_tracks_id = results[i]['track']['id']
                playlist_tracks_titles = results[i]['track']['name']
                playlist_tracks_first_release_date = results[i]['track']['album']['release_date']
                playlist_tracks_popularity = results[i]['track']['popularity']
                artist_list = []
                for artist in results[i]['track']['artists']:
                    artist_list = artist['name']
                playlist_tracks_artists = artist_list
                features = sp.audio_features(playlist_tracks_id)
                new_row = {'id': [playlist_tracks_id],
                           'title': [playlist_tracks_titles],
                           'all_artists': [playlist_tracks_artists],
                           'popularity': [playlist_tracks_popularity],
                           'release_date': [playlist_tracks_first_release_date],
                           'danceability': [features[0]['danceability']],
                           'energy': [features[0]['energy']],
                           'key': [features[0]['key']],
                           'loudness': [features[0]['loudness']],
                           'mode': [features[0]['mode']],
                           'acousticness': [features[0]['acousticness']],
                           'instrumentalness': [features[0]['instrumentalness']],
                           'liveness': [features[0]['liveness']],
                           'valence': [features[0]['valence']],
                           'tempo': [features[0]['tempo']],
                           'duration_ms': [features[0]['duration_ms']],
                           'time_signature': [features[0]['time_signature']]
                           }

                dfs = [features_df, pd.DataFrame(new_row)]
                features_df = pd.concat(dfs, ignore_index=True)
            except:
                continue

    return features_df


if __name__ == '__main__':
    music_data = data_scraping()
    music_data.to_csv("playlist_" + str("spotify_top50Global_today") + ".csv", encoding='utf-8', index="false")
