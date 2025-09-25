from flask import Flask, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, Api, abort
from schemas import TodoSchema
from models import Todo, Session

# Flask 애플리케이션 설정
app = Flask(__name__)
app.config["API_TITLE"] = "할 일 목록 API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# API 블루프린트 생성
blp = Blueprint("todos", __name__, url_prefix="/todos", description="할 일 관련 작업")

@blp.route("/")
class TodoList(MethodView):
 @blp.response(200, TodoSchema(many=True))
 def get(self):
 """전체 할 일 목록 조회"""
 session = Session()
 todos = session.query(Todo).all()
 session.close()
 return todos

 @blp.arguments(TodoSchema)
 @blp.response(201, TodoSchema)
 def post(self, new_todo_data):
 """새로운 할 일 추가"""
 session = Session()
 new_todo = Todo(**new_todo_data)
 session.add(new_todo)
 session.commit()
 session.refresh(new_todo)
 session.close()
 return new_todo

@blp.route("/<int:todo_id>")
class Todo(MethodView):
 @blp.response(200, TodoSchema)
 def get(self, todo_id):
 """특정 할 일 조회"""
 session = Session()
 todo = session.query(Todo).get(todo_id)
 if todo is None:
 abort(404, message="할 일을 찾을 수 없습니다.")
 session.close()
 return todo

 @blp.arguments(TodoSchema)
 @blp.response(200, TodoSchema)
 def put(self, update_data, todo_id):
 """특정 할 일 수정"""
 session = Session()
 todo = session.query(Todo).get(todo_id)
 if todo is None:
 abort(404, message="할 일을 찾을 수 없습니다.")

 for key, value in update_data.items():
 setattr(todo, key, value)
 
 session.commit()
 session.close()
 return todo

 @blp.response(204)
 def delete(self, todo_id):
 """특정 할 일 삭제"""
 session = Session()
 todo = session.query(Todo).get(todo_id)
 if todo is None:
 abort(404, message="할 일을 찾을 수 없습니다.")

 session.delete(todo)
 session.commit()
 session.close()
 return ""

api.register_blueprint(blp)

if __name__ == "__main__":
 app.run(debug=True)