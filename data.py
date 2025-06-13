import pandas as pd

# 엑셀 파일 읽기
def load_comics():
    df = pd.read_excel("comics.csv")
    return df.to_dict(orient="records")  # 리스트로 변환

def load_lps():
    df = pd.read_excel("lps.csv")
    return df.to_dict(orient="records")
