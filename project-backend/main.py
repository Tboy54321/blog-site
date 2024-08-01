from fastapi import FastAPI
from routers import blogs

app = FastAPI()


app.include_router(blogs.router)

@app.get('/')
def home():
  return {"Home": "My blog home project"}
