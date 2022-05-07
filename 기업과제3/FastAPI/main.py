import os
import torch
import uvicorn
import preprocessing as pp 
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

# 현재 파일이 실행되고 있는 경로
_CUR_PATH = os.getcwd()

app = FastAPI()

### Pre-Load ###
# check device
if torch.cuda.is_available():
    device = torch.device('cuda')
else :
    device = torch.device('cpu')

# model pre-load
_MODEL_PATH = os.path.join(_CUR_PATH, 'kor_sts_klue-roberta-base-2022-03-21_03-51-02')
model = SentenceTransformer(_MODEL_PATH, device=device)

class Data(BaseModel):
    sentence1 : str # 문장1
    sentence2 : str # 문장2

@app.post("/")
def semantic_textual_similarity(sentence1, sentence2):
    # 문장 전처리
    sentence1 = pp.clean_text(sentence1) 
    sentence2 = pp.clean_text(sentence2)
    # 문장 embedding
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)
    # 코사인 유사도 결과
    cosine_score = util.cos_sim(embedding1, embedding2) # Range : -1 ~ 1
    # 유사도 범위를 0~5사이로 조절
    label_temp = torch.clip(cosine_score, min=0) * 5 # Range : 0~5
    # label이 3이상이면 유사한 것으로 판단 그 외는 관계없음
    if label_temp >= 3:
        label = "유사"
    else:
        label = "관계없음"
    # 입력받은 2문장과 label 반환
    return {"Sentence1" : sentence1, "Sentence2" : sentence2, "Label" : label}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)