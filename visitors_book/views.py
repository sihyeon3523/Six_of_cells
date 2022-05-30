from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings

import pandas as pd
from . import predict_sentiment_func
import re

# Create your views here.
# def index(request):
#     return render(request, 'visitors_book/base.html', {})



def visitors_book(request):

    current_time = timezone.now()
    context = {'current_time':current_time}

    return render(request, 'visitors_book/base.html', context) #base.html 방명록 글 시간에 넣을 것임



#kobert 모델에 사용자 인풋 넣어서 확률 얻기
def today_emotion(request):
    try:
                                        #base.html에서 사용자가 입력한 글
        target_sentence = request.POST['target_sentence']

        user_input = str(target_sentence)

        # 문장 분리
        input_list = user_input.split(".")

        #정제된 문장들 담을 빈 리스트
        processed_input = []
        for sentence in input_list:
            output_string = re.sub(r'[^\w\s]', '', sentence)
            processed_input.append(output_string)

        tokenizer = settings.TOKENIZER_KOBERT
        model = settings.MODEL_KOBERT

        total_array, top_pred_prob, top_pred_class, total_array_emotions = predict_sentiment_func.predict_sentiment_user(processed_input, tokenizer, model)

        context = {'total_array': total_array, 'top_pred_prob': top_pred_prob, 'top_pred_class':top_pred_class, 'total_array_emotions': total_array_emotions}

    except:
        context = {"error_message": "방명록을 입력해주세요."}

    return render(request, 'visitors_book/today_emotion.html', context)
