from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from . import music_similarity

# Create your views here.
def music_choice(request):
    user_name = request.POST['user_name']
    total_array = request.POST["total_array"]

    happiness = pd.read_csv("./data/happiness.csv", encoding='utf-8', lineterminator='\n')
    anger = pd.read_csv("./data/anger.csv", encoding='utf-8', lineterminator='\n')
    sadness = pd.read_csv("./data/sadness.csv", encoding='utf-8', lineterminator='\n')
    surprise = pd.read_csv("./data/surprise.csv", encoding='utf-8', lineterminator='\n')

    happiness = happiness[['Title','Artist']]
    anger = anger[['Title','Artist']]
    sadness = sadness[['Title','Artist']]
    surprise = surprise[['Title','Artist']]

    #비복원 추출
    hap_2 = happiness.sample(n=2, replace=False)
    ang_2 = anger.sample(n=2, replace=False)
    sad_2 = sadness.sample(n=2, replace=False)
    sur_2 = surprise.sample(n=2, replace=False)

    #랜덤추출한 곡 담은 df
    random_songs_df = pd.concat([hap_2,ang_2,sad_2,sur_2])

    random_songs_list = []
    for row in random_songs_df.iterrows():
    #     print(row[1][0]) #제목
    #     print(row[1][1]) #가수

        random_songs_list.append((row[1][0],row[1][1]))

    context = {'random_songs_list':random_songs_list, 'total_array':total_array, "user_name":user_name}


    return render(request, 'music_choice/music_choice.html', context)

def recommendation(request):
    user_name = request.POST['user_name']
    seed_song = request.POST.getlist("answer[]")

    recom_songs_list = []

    if seed_song == []:
        random_df = music_similarity.random_recom()

        for row in random_df.iterrows():
            recom_songs_list.append((row[1][0],row[1][2])) #(제목, 가수)

        context = {"user_name":user_name,"recom_songs_list":recom_songs_list}
        return render(request, 'music_choice/recommendation.html', context)

    song_recom = music_similarity.find_simi_song(seed_song,6)
    total_array = request.POST["total_array"]
    emotion_recom = music_similarity.user_song_simi(song_recom,total_array)


    for row in emotion_recom.iterrows():
        recom_songs_list.append((row[1][0],row[1][2]))

    context = {"user_name":user_name,"recom_songs_list":recom_songs_list}

    return render(request, 'music_choice/recommendation.html', context)

# def recommendation(request):
#     user_name = request.POST['user_name']
#     seed_song = request.POST.getlist("answer[]")
#
#     song_recom = music_similarity.find_simi_song(seed_song,6)
#
#     total_array = request.POST["total_array"]
#
#     emotion_recom = music_similarity.user_song_simi(song_recom,total_array)
#
#     recom_songs_list = []
#     for row in emotion_recom.iterrows():
#     #     print(row[1][0]) #제목
#     #     print(row[1][2]) #가수
#
#         recom_songs_list.append((row[1][0],row[1][2]))
#
#
#     context = {"recom_songs_list":recom_songs_list, "user_name":user_name}
#
#     return render(request, 'music_choice/recommendation.html', context)
