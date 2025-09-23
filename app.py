from flask import Flask, render_template

# Flask 애플리케이션 생성
app = Flask(__name__)

# 사용자 데이터 정의
users = [
    {"username": "traveler", "name": "Alex"},
    {"username": "photographer", "name": "Sam"},
    {"username": "gourmet", "name": "Chris"}
]

# 루트 URL('/')에 접속했을 때 실행될 함수
@app.route('/')
def index():
    return render_template("index.html", users=users)


# 프로그램 실행 (python app.py 했을 때만 실행되도록 함)
if __name__ == "__main__":
    app.run(debug=True)
