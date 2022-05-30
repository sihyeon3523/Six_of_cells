from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.
def music_choice(request):

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

    context = {'random_songs_list':random_songs_list}


    return render(request, 'music_choice/music_choice.html', context)


def recommendation(request):
    return render(request, 'music_choice/recommendation.html', {})



# from django.shortcuts import render
# from django.http import HttpResponse
#
# # Create your views here.
# def music_choice(request):
#
#     return render(request, 'music_choice/music_choice.html', {})
#
# def recommendation(request):
#     return render(request, 'music_choice/recommendation.html', {})
