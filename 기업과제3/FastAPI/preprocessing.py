import re

def clean_text(text):
    review = re.sub(r'\s+', ' ', str(text))  #과다한 띄어쓰기를 한번의 띄어쓰기로 변경
    review = review.lower() #영어 일단 소문자화
    review = re.sub(r'<[^>]+>','',review) #Html tags 제거
    review = re.sub(r'[^ A-Za-z0-9가-힣+]','',review) #특수문자 제거
    review = re.sub(r'\s+', ' ', review) #과다한 띄어쓰기를 한번의 띄어쓰기로 변경22
    review = re.sub(r"^\s+", '', review) #띄어쓰기로 시작하는 것 제거
    review = re.sub(r'\s+$', '', review) #띄어쓰기로 끝나는 것 제거
    return review