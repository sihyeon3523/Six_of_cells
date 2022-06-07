# Contents

[1. Index](#1.-index)

[2. visitors book](#2.-visitors-book)

[3. music choice](#3.-music-choice)

<hr>


##1. Index
<img width="80%" src="https://user-images.githubusercontent.com/49083528/172381153-358b463c-1b40-4436-a740-d0d76d553409.png"/>

  - 유저 이름 입력   

  - <form>태그로 url '/visitors_book/'에 POST 요청   

<br>

##2. visitors book
<img width="80%" src="https://user-images.githubusercontent.com/49083528/172381303-d0cdd8b4-d987-4b9f-91fb-78f13ce817ed.png"/>
  
  - views.visitors_book를 통해 호출하면서 timezone.now()로 현재시간을 가져와 방명록 작성시간 보여줌   
  
  - 유저가 300자 이내의 한글 텍스트 입력 
  
  - 입력하지 않고 submit하면 에러 메시지 뜨게 함
  
  - <form>태그로 url '/today_emotion/'에 POST 요청   

<br>

## 2.1 emotion dashboard
<img width="80%" src="https://user-images.githubusercontent.com/49083528/172381386-98945b0a-5f31-4b6c-afb8-b15a0e126c21.png"/>
  
  - POST 요청으로 받은 텍스트를 views.today_emotion에서 기존에 학습시킨 KoBERT 모델로 문장단위 감정 분석하여 4개 감정별 확률값을 얻음   
  
  - 싸이월드 감성분류 아이콘을 활용해 유저가 입력한 글을 KoBERT로 감정분석한 결과 보여줌   
  
<br>

##3. music choice
<img width="80%" src="https://user-images.githubusercontent.com/49083528/172381522-1fb2add5-f381-4801-adf8-b649d99146ce.png"/>
  
  - 감정별 플레이리스트가 담긴 csv파일에서 2곡씩 랜덤추출하여 사용자에게 보여주고 3곡 선택하게 함
  
  - 3곡 이상 선택하면 에러 메시지 뜨게 함
  
  - 곡 리스트 새로고침 기능
  
<br>

## 3.1 music recommendation
<img width="80%" src="https://user-images.githubusercontent.com/49083528/172381564-07a774ef-ab02-43a0-9b10-9d4294723d00.png"/>
  
  - visitors_book/today_emotion에서 KoBERT로 유저 감정분석한 감정별 4개 확률값 & 기존에 곡 가사를 문장단위로 감정분석해둔 감정별 4개 확률값 & 유저가 선택한 곡과의 장르/가수/가사 유사도분석을 활용한 추천알고리즘으로 5개 곡 추천  
  
  
  
