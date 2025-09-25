from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite 데이터베이스 파일 생성 (todo.db)
engine = create_engine("sqlite:///todo.db", echo=True)
Base = declarative_base()

class Todo(Base):
 __tablename__ = 'todos'

 id = Column(Integer, primary_key=True)
 task = Column(String, nullable=False)
 completed = Column(Boolean, default=False)

 def __repr__(self):
 return f"<Todo(id={self.id}, task='{self.task}')>"

# 모든 테이블 생성
Base.metadata.create_all(engine)

# 데이터베이스 세션을 만들고 바인딩
Session = sessionmaker(bind=engine)