from pydantic import BaseModel


class blogsBase(BaseModel):
  title: str

class blogsOut(blogsBase):
  id: int