from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# 실행 경로 기준으로 엑셀 파일 경로 설정
base_path = os.path.dirname(os.path.abspath(__file__))
comics_path = os.path.join(base_path, 'comics.csv')
lps_path = os.path.join(base_path, 'lps.csv')

# 엑셀 파일에서 도서(만화책) 데이터 읽기
comics_data = pd.read_csv(comics_path)

# 홈 페이지 (버튼 2개만 있는 화면)
@app.route('/')
def home():
    return render_template('home.html')

# 도서 검색 페이지
@app.route('/book_search', methods=['GET', 'POST'])
def book_search():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        # 검색 기능: comics_data에서 'name' 열을 기준으로 keyword를 포함한 항목을 찾기
        results = comics_data[comics_data['name'].str.contains(keyword, case=False, na=False)]
        results = results.to_dict(orient='records')  # 결과를 dict 형식으로 변환
    return render_template('book_search.html', results=results)

# LP 검색 페이지 (경로를 /lp_search로 수정)
@app.route('/lp_search', methods=['GET', 'POST'])
def lp_search():
    results = None
    if request.method == 'POST':
        keyword = request.form['keyword'].lower()  # 입력받은 검색어를 소문자로 변환
        df = pd.read_excel(lps_path)  # LP 엑셀 데이터 읽기

        # 'title', 'singer', 'location' 열 중 하나라도 keyword를 포함한 항목을 필터링
        filtered = df[
            df['title'].astype(str).str.lower().str.contains(keyword, na=False) |
            df['singer'].astype(str).str.lower().str.contains(keyword, na=False) |
            df['location'].astype(str).str.lower().str.contains(keyword, na=False)
        ]

        # 필터링된 결과를 리스트로 변환
        results = [
            {'name': f"{row['title']} - {row['singer']}", 'location': row['location']}
            for index, row in filtered.iterrows()
        ]
        
    # 결과를 lp_search.html 템플릿으로 전달
    return render_template('lp_search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)