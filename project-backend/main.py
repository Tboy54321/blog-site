from fastapi import FastAPI
from routers import blogs, users, auth, likes, comments, notifications

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
