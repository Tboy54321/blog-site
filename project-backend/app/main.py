from fastapi import FastAPI
# from routers import blogs, users, auth, likes, comments, notifications [UVICORN]
from app.routers import blogs, users, auth, likes, comments, notifications
# import app.models as models
# from app.database import engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(blogs.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(likes.router)
app.include_router(comments.router)
app.include_router(notifications.router)

@app.get('/')
def home():
  return {"Home": "My blog home project"}
