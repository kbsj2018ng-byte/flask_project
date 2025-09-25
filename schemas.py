from marshmallow import Schema, fields

class TodoSchema(Schema):
 id = fields.Int(dump_only=True)  # 데이터베이스에서 생성될 ID
 task = fields.Str(required=True, description="할 일 내용")
 completed = fields.Bool(load_default=False, description="완료 여부")