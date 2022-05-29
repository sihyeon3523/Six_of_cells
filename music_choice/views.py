from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.
def music_choice(request):

    happiness = pd.read_csv("./data/happiness.csv", encoding='utf-8', lineterminator='\n')
    anger = pd.read_csv("./data/anger.csv", encoding='utf-8', lineterminator='\n')
    sadness = pd.read_csv("./data/sadness.csv", encoding='utf-8', lineterminator='\n')
    surprise = pd.read_csv("./data/surprise.csv", encoding='utf-8', lineterminator='\n')

    #비복원 추출
    hap_2 = happiness.sample(n=2, replace=False)
    ang_2 = anger.sample(n=2, replace=False)
    sad_2 = sadness.sample(n=2, replace=False)
    sur_2 = surprise.sample(n=2, replace=False)

    #랜덤추출한 곡을 담은 df
    random_songs_df = pd.concat([hap_2,ang_2,sad_2,sur_2])

    context = {'random_songs_df':random_songs_df}

    # for row in random_songs_df.iterrows():
    #     title = row[1][2] #제목
    #     artist = row[1][3] #가수

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
