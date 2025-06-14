import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# app.py 파일 위치 기준으로 data 폴더 내 CSV 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))  # app.py의 절대 경로
comics_path = os.path.join(base_dir, 'data', 'comics.csv')  # comics.csv 경로 설정
lps_path = os.path.join(base_dir, 'data', 'lps.csv')  # lps.csv 경로 설정

# CSV 데이터 로드 (인코딩 cp949로 변경)
comics_data = pd.read_csv(comics_path, encoding='cp949')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/book_search', methods=['GET', 'POST'])
def book_search():
    results = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        results = comics_data[comics_data['name'].str.contains(keyword, case=False, na=False)]
        results = results.to_dict(orient='records')
    return render_template('book_search.html', results=results)

@app.route('/lp_search', methods=['GET', 'POST'])
def lp_search():
    results = None
    if request.method == 'POST':
        keyword = request.form['keyword'].lower()
        df = pd.read_csv(lps_path, encoding='cp949')  # lps.csv도 인코딩 맞춰 변경
        filtered = df[
            df['title'].astype(str).str.lower().str.contains(keyword, na=False) |
            df['singer'].astype(str).str.lower().str.contains(keyword, na=False) |
            df['location'].astype(str).str.lower().str.contains(keyword, na=False)
        ]
        results = [{'name': f"{row['title']} - {row['singer']}", 'location': row['location']} for _, row in filtered.iterrows()]
    return render_template('lp_search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
