import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def find_simi_song(seed_song,top_n=10):

    song_df = pd.read_csv("./data/song_total.csv",index_col=0)
    song_simi_co_sorted_df = pd.read_csv("./data/song_similarity.csv",index_col=0)
    song_simi_co_sorted = np.array(song_simi_co_sorted_df)

    song_recom=pd.DataFrame(columns=song_df.columns)

    for seed in seed_song:
        title=song_df[song_df["Title"] == seed]
        title_index=title.index.values
        similar_indexes = song_simi_co_sorted[title_index,:top_n]
        similar_indexes = similar_indexes.reshape(-1)
        song_recom=pd.concat([song_recom,song_df.iloc[similar_indexes].iloc[1:,:]])

    return song_recom

def user_song_simi(song_recom,total_array):

    song_emotion=np.array(song_recom[['분노혐오', '놀람공포', '슬픔', '행복']])

    # total_array 문자열 -> numpy 배열
    total_array_list=list(total_array[2:-2].split())
    total_array_list=list(map(float,total_array_list))
    total_array=np.array([total_array_list])

    song_user_cosine_index=cosine_similarity(total_array,song_emotion).argsort()[:, ::-1]
    song_recom_index=song_user_cosine_index.reshape(-1)[:5]


    return song_recom.iloc[song_recom_index]
