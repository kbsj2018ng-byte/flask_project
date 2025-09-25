# schemas.py
from marshmallow import Schema, fields

# 책의 정보를 담을 설계도(Schema)를 만들어요.
# 이 설계도는 책이 'title'과 'author'라는 두 가지 정보를 가질 거라고 알려줘요.
class BookSchema(Schema):
    # 'title'은 글자(string)여야 해요.
    title = fields.Str(required=True, description="책의 제목")
    # 'author'도 글자(string)여야 해요.
    author = fields.Str(required=True, description="책의 저자")