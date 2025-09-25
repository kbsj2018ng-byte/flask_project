# app.py
global book_id_counter 
from flask import Flask
from flask.views import MethodView
from flask_smorest import Blueprint, Api
from schemas import BookSchema

# 우리 도서관을 만들기 위해 Flask 앱을 시작해요.
app = Flask(__name__)
# API 문서화를 위한 설정을 추가해요.
app.config["API_TITLE"] = "책 관리 API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# API를 만들 준비를 해요.
api = Api(app)

# 'books'라는 이름의 새로운 창구를 만들어요.
blp = Blueprint("books", __name__, url_prefix="/books", description="책 관련 작업")

# 도서관에 있는 책들을 잠시 담아둘 목록(리스트)을 만들어요.
# 지금은 책이 없어요.
BOOKS = []
book_id_counter = 1

# 'Book'이라는 도서관 관리자를 만들 거예요.
# 이 관리자는 손님의 요청에 따라 책을 찾아주거나, 넣어주거나, 바꿔주거나, 없애주는 일을 해요.
@blp.route("/")
class Book(MethodView):
    # 📚 GET 요청: 도서관에 있는 모든 책 목록을 보여줘!
    @blp.response(200, BookSchema(many=True))
    def get(self):
        # 모든 책 목록을 손님에게 보여줘요.
        return BOOKS

    # ✍️ POST 요청: 새 책을 도서관에 넣어줘!
    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
   # app.py의 post 메서드
    def post(self, new_book_data):
    
    
    new_book_data["id"] = book_id_counter
    
    BOOKS.append(new_book_data)
    book_id_counter += 1
    return new_book_data

@blp.route("/<int:book_id>")
class BookDetail(MethodView):
    # 🔍 GET 요청: 특정 번호의 책을 찾아줘!
    @blp.response(200, BookSchema)
    def get(self, book_id):
        # 책 목록에서 번호에 맞는 책을 찾아줘요.
        book = next((book for book in BOOKS if book["id"] == book_id), None)
        # 만약 책이 없으면 에러를 내보내요.
        if book is None:
            blp.abort(404, message="책을 찾을 수 없어요.")
        return book

    # ✏️ PUT 요청: 특정 번호의 책 정보를 바꿔줘!
    @blp.arguments(BookSchema)
    @blp.response(200, BookSchema)
    def put(self, update_data, book_id):
        # 책 목록에서 번호에 맞는 책을 찾아요.
        book = next((book for book in BOOKS if book["id"] == book_id), None)
        # 만약 책이 없으면 에러를 내보내요.
        if book is None:
            blp.abort(404, message="책을 찾을 수 없어요.")
        # 찾은 책의 정보를 새로운 정보로 바꿔줘요.
        book.update(update_data)
        return book

    # 🗑️ DELETE 요청: 특정 번호의 책을 없애줘!
    @blp.response(204)
    def delete(self, book_id):
        global BOOKS
        # 책 목록에서 번호에 맞는 책을 빼버려요.
        BOOKS = [book for book in BOOKS if book["id"] != book_id]
        # 성공적으로 지웠다고 알려줘요. (내용이 없어도 돼요)
        return ""

# 마지막으로, 'books' 창구를 우리 도서관에 연결해요.
api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True)