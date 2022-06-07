1. KoBERT_keras_2
2. KoBERT_keras_2_del_neu
3. KoBERT_keras_2_netral_undersampling
4. KoBERT_4_labels
5. emotion_base_recommnedation

<br>
# KoBERT

## 0. Introdunction

- colab 환경에서 진행되었습니다
- TPU, HuggingFace의 Transformers, SKTBrain의 KoBERT tokenizer & model을 활용해 진행하였고, random seed는 1234로 고정했습니다

<br>

### 0.1 Source Data

- 7종 감정 라벨링<br>
  분노, 놀람, 행복, 슬픔, 혐오, 공포, 중립<br>

- [한국어 감정 정보가 포함된 단발성 대화 데이터](https://aihub.or.kr/opendata/keti-data/recognition-laguage/KETI-02-009)

- [한국어 감정 정보가 포함된 연속적 대화 데이터셋](https://aihub.or.kr/opendata/keti-data/recognition-laguage/KETI-02-010)

- [감정 분류를 위한 대화 음성 데이터셋](https://aihub.or.kr/opendata/keti-data/recognition-laguage/KETI-02-002)

<br>

## 1. Pre-Process Data

### 1) re-labeling
- 가사 감정분석의 목적에 맞게 '중립' 라벨 제거, '분노'와 '혐오' 그리고 '놀람'과 '공포' 라벨을 합쳤습니다

- Class Distribution
  - 분노혐오    20526
  - 놀람공포    19471
  - 행복       11615
  - 슬픔       10087

<img width="40%" height="40%" src="https://user-images.githubusercontent.com/78069770/171363414-a8871cfb-31a0-4bee-b3f7-9e323c854fe5.png">

- Digitizing Label<br>
  - 분노+혐오 : 0 
  - 놀람+공포 : 1
  - 슬픔 : 2
  - 행복 : 3

### 2) Split Data to Train & Test

- 총 61,699행의 전체 데이터 중 20%를 test 데이터로 분리해주었습니다

### 3) Load Tokenizer & Apply on Train Data

- 전체 데이터 중 문장길이 상위 5개를 토큰화한 결과, 토큰 최댓값이 292임에 따라 임의값인 300을 sequence의 최대길이로 설정하였습니다

- encode_plus 함수를 이용해 train data를 BERT input 형태(tokens_tensor, segments_tensor, masks_tensor)로 전처리했습니다

<br>

## 2. Modeling<br>

### 1) Create Model<br>
<img width="80%" height="80%" src="https://user-images.githubusercontent.com/78069770/171365220-137bec78-48b0-4220-8b7d-66f9d5595f30.png">

- overfitting으로 Dropout(0.2)를 추가해주었습니다
- optimizer는 RectifiedAdam, Crossentropy과 Accuracy는 모두 SparseCategorical를 사용했습니다
- learning_rate 는 1e-5로 진행했습니다


### 2) TPU setting before Training

- 훈련에 TPU를 활용하기 위해 TPU cluster 할당과 초기화 후, 모델의 compile까지 TPU strategy scope 내에서 생성했습니다 

<br>

## 3. Train

### 1) Setting Checkpoint & EarlyStopping
- 좋은 결과를 낸 모델의 가중치를 저장하기 위해 Checkpoint를, overfitting을 예방하기 위해 EarlyStopping을 생성했습니다

### 2) train
- validation split은 0.2로, epoch와 batch size는 각각 7, 100으로 진행했습니다

### 3) Result
- train data 
  -   loss: 0.5072 
  -   sparse_categorical_accuracy: 0.8070 <br>
- validation data
  -   loss: 0.6786
  -   sparse_categorical_accuracy: 0.7456
  
<br>

## 4. Test
- test data 또한 input 형태로 전처리한 후, Checkpoint로 저장된 모델을 load해 테스트를 진행했습니다
- Result
  - **Accuracy** : 0.7503
  - **Classification Report** <br>
    <img width="80%" height="80%" src="https://user-images.githubusercontent.com/78069770/171368266-c7752f90-9d00-4299-b9cd-152180bebc5e.png"> 

<br>

## 5. Save Model
- 추후 분석에 이용하기 위해 pickle 파일로 저장했습니다

<br>

## 6. Load Saved Model

- pickle 파일 load, input 데이터로 전처리, 분석의 코드입니다

<br>

# emotion_base_recommendation
<br>
## 0. Introdunction
1. 사용자가 선택한 노래와 가장 유사한 노래를 찾는다.
2. 유사한 노래 중 사용자의 감정과 가장 비슷한 노래를 추천해준다.
<br>
## 1. Data Load
- sample_songlist.csv : 가사 띄어쓰기가 잘 되어있는 노래 정보 데이터
- df_final_lyrics.csv : 노래의 가사에 대한 4가지 감정이 태깅되어 있는 데이터
- sample_songlist.csv 의 제목과 가수를 기준으로 두 csv 파일을 합친다.
<br>
## 2. Data Exploration
- 가사가 "슬픔"으로 분류되는 감정이 가장 많은 장르는 발라드이다.
- 가사가 "분노혐오"로 분류되는 감정이 가장 많은 장르는 발라드이다.
<br>
## 3. Song similarity
- 노래 간의 유사도를 구하기 위해 다음을 이용한다.
1. Genre Similarity by Countervectorizer & Cosine_Similarity
2. Lyrics Similarity by Tfidfvectorizer & Cosine_Similarity
- 임의로 가중치 부여
song_simi_co = (
                 + song_simi_genre * 0.3 # 가중치 0.3 * 장르 유사도
                 + song_simi_lyric * 1 # 가중치 1 * 가사 유사도
                 )
-> 가사의 유사도가 낮고, 가사의 감정 기반으로 추천하기 때문에 유사도를 높게 설정했다.
<br>

## 4. Song Recommendation (in Django)
- 사용자가 선택한 노래에서 3에서 구한 유사도 값이 큰 노래를 뽑는다.
- 유사도 값이 큰 노래 중 사용자의 감정과 가장 유사한 노래를 뽑는다.
1. 사용자의 감정을 numpy 배열로 변환한다.
2. 사용자의 감정 확률 값과 유사한 노래 감정 확률의 유사도를 Cosine Similarity로 구한다.
3. Cosine Similarity 값이 큰 노래 5곡을 추천한다.
<br>




