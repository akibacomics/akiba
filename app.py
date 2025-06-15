import os
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
comics_path = os.path.join(base_dir, 'data', 'comics.csv')
lps_path = os.path.join(base_dir, 'data', 'lps.csv')

# 글로벌 변수로 데이터 로드
comics_data = pd.read_csv(comics_path, encoding='cp949')
lps_data = pd.read_csv(lps_path, encoding='cp949')

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
        filtered = lps_data[
            lps_data['title'].astype(str).str.lower().str.contains(keyword, na=False) |
            lps_data['singer'].astype(str).str.lower().str.contains(keyword, na=False) |
            lps_data['location'].astype(str).str.lower().str.contains(keyword, na=False)
        ]
        results = [{'name': f"{row['title']} - {row['singer']}", 'location': row['location']} for _, row in filtered.iterrows()]
    return render_template('lp_search.html', results=results)

# 여기에 CSV 데이터 다시 읽는 API 추가
@app.route('/api/update-csv', methods=['POST'])
def update_csv():
    global comics_data, lps_data
    try:
        comics_data = pd.read_csv(comics_path, encoding='cp949')
        lps_data = pd.read_csv(lps_path, encoding='cp949')
        return jsonify({"message": "CSV 데이터가 성공적으로 업데이트되었습니다."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
