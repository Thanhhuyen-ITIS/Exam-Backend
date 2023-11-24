from fastapi import  FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

import models
from config.database import engine
from router import authentication, user_route, topic_route, test_route, answer_of_user_route, answer_route, \
    attemp_route, question_route, result_route, test_detail_route, topic_detail_route, test_user_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Địa chỉ nguồn gốc của trình duyệt
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Cho phép tất cả các header
)

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user_route.router)
app.include_router(topic_route.router)
app.include_router(test_route.router)
app.include_router(answer_of_user_route.router)
app.include_router(answer_route.router)
app.include_router(attemp_route.router)
app.include_router(question_route.router)
app.include_router(result_route.router)
app.include_router(test_detail_route.router)
app.include_router(topic_detail_route.router)
app.include_router(test_user_route.router)

add_pagination(app)

