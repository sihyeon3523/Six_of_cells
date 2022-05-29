import re
import numpy as np

def predict_sentiment_sentence(sentence, tokenizer, model):
    SEQ_LEN = 300

    # Tokenizing / Tokens to sequence numbers / Padding
    encoded_dict = tokenizer.encode_plus(text=re.sub("[^\s0-9a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣]", "", sentence), # 특수문자 제거
                                         padding='max_length',
                                         truncation = True,
                                         max_length=SEQ_LEN)

    token_ids = np.array(encoded_dict['input_ids']).reshape(1, -1)
    token_masks = np.array(encoded_dict['attention_mask']).reshape(1, -1)
    token_segments = np.array(encoded_dict['token_type_ids']).reshape(1, -1)

    new_inputs = (token_ids, token_masks, token_segments)

    # Prediction
    pred = model.predict(new_inputs)
    all_pred_proba = np.round(pred * 100, 2)

    return all_pred_proba


def predict_sentiment_user(sentence_list, tokenizer, model):

    for sentence in sentence_list:
        all_pred_proba = predict_sentiment_sentence(sentence, tokenizer, model)
        anger = all_pred_proba[0][0]
        scary = all_pred_proba[0][1]
        sad = all_pred_proba[0][2]
        happy = all_pred_proba[0][3]

        anger += anger
        scary += scary
        sad  += sad
        happy += happy

    #분석된 4개 감정별 확률
    total_array = np.ndarray.round( (np.array([(anger, scary, sad, happy)]) / (anger + scary + sad + happy)), 2)
    #가장 높은 확률값
    top_pred_prob = total_array[0][np.argmax(total_array, axis=1)[0]]
    #가장 높은 확률의 감정
    top_pred_class = ['분노혐오','놀람공포','슬픔','행복'][np.argmax(total_array, axis=1)[0]]

    return total_array, top_pred_prob, top_pred_class
