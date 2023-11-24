from sqlalchemy import Column, Integer, String, ForeignKey, BLOB, Float, Text, Boolean
from sqlalchemy.dialects.mssql import JSON
from sqlalchemy.orm import relationship

from config.database import Base
from sqlalchemy.types import DATE, DATETIME


class Role(Base):
    __tablename__ = 'tbl_role'

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(20))

#role, user, question, contest

class User(Base):
    __tablename__ = 'tbl_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), nullable=False, unique=True)
    email = Column(String(45))
    password = Column(String(200), nullable=False)
    name = Column(String(45))
    id_role = Column(Integer, ForeignKey('tbl_role.id'), default=2)

    role = relationship("Role", backref="users")

class Topic(Base):
    __tablename__ = 'tbl_topic'
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_name = Column(String(200))
    topic_image = Column(Text(4294967295))
    create_time = Column(DATETIME)



class Test(Base):
    __tablename__ = 'tbl_test'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_name = Column(String(200))
    start_time = Column(DATETIME)
    end_time = Column(DATETIME)
    duration = Column(Integer)
    limit = Column(Integer, default=0)
    permission_review = Column(Boolean, default=False)



class Question(Base):
    __tablename__ = 'tbl_question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(String(45), nullable=False, unique=True)
    question_content = Column(String(200), nullable=False)


class TestTopic(Base):
    __tablename__ = 'tbl_testtopic'
    id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey('tbl_topic.id'))
    test_id = Column(Integer, ForeignKey('tbl_test.id'))

    topic = relationship("Topic", backref="test_topics")
    test = relationship("Test", backref="test_topics")

class QuestionTest(Base):
    __tablename__ = 'tbl_questiontest'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey('tbl_test.id'))
    question_id = Column(Integer, ForeignKey('tbl_question.id'))

    test = relationship("Test", backref="question_tests")
    question = relationship("Question", backref="question_tests")

class Answer(Base):
    __tablename__ = 'tbl_answer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('tbl_question.id'))
    answer_item = Column(String(1))
    answer_content = Column(String(200))
    is_correct_answer = Column(Boolean, default=False)

    question = relationship("Question", backref="answers")

class Result(Base):
    __tablename__ = 'tbl_result'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('tbl_user.id'))
    test_id = Column(Integer, ForeignKey('tbl_test.id'))
    start_time = Column(DATETIME)
    end_time = Column(DATETIME)
    score = Column(Float)
    completion_time = Column(Integer)

    user = relationship("User", backref="results")
    test = relationship("Test", backref="results")


class AnswerOfUser(Base):
    __tablename__ = 'tbl_answerofuser'

    id = Column(Integer, primary_key=True, autoincrement=True)
    result_id = Column(Integer, ForeignKey('tbl_result.id'))
    question_id = Column(Integer, ForeignKey('tbl_question.id'))
    answer = Column(JSON)
    is_correct = Column(Boolean, default=True)

    result = relationship("Result", backref="answer_of_users")
    question = relationship("Question", backref="answer_of_users")

class TestUser(Base):
    __tablename__ = 'tbl_testuser'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('tbl_user.id'))
    test_id = Column(Integer, ForeignKey('tbl_test.id'))
    count = Column(Integer, default=0)
    
    user = relationship("User", backref="test_users")
    test = relationship("Test", backref="test_users")
