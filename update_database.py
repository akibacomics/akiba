import schedule
import time
import pandas as pd
from sqlalchemy import create_engine

# 데이터베이스 연결
# 실제 데이터베이스 정보로 바꿔주세요.
db_url = 'postgresql://postgres:comis1110akiba@localhost:5432/comics'  # comics 데이터베이스 사용
engine = create_engine(db_url)

# CSV 파일을 데이터베이스에 반영하는 함수
def update_database():
    # comics.csv 파일 읽기
    comics_df = pd.read_csv(r'C:\akibacomics-main\akibacomics\comics.csv')
    comics_df.to_sql('comics', engine, if_exists='replace', index=False)  # 'comics' 테이블에 덮어쓰기

    # lp.csv 파일 읽기
    lp_df = pd.read_csv(r'C:\akibacomics-main\akibacomics\lp.csv')
    lp_df.to_sql('lp', engine, if_exists='replace', index=False)  # 'lp' 테이블에 덮어쓰기

# 매 10분마다 CSV 파일을 읽고 데이터베이스를 업데이트
schedule.every(10).minutes.do(update_database)

# 실행
while True:
    schedule.run_pending()
    time.sleep(1)

