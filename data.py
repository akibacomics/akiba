import pandas as pd

# 엑셀 파일 읽기
def load_comics():
    df = pd.read_excel("comics.xlsx")
    return df.to_dict(orient="records")  # 리스트로 변환

def load_lps():
    df = pd.read_excel("lps.xlsx")
    return df.to_dict(orient="records")
