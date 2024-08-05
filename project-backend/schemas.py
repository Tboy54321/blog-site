from pydantic import BaseModel, EmailStr


class blogsBase(BaseModel):
  title: str

class blogsOut(blogsBase):
  id: int

class UserBase(BaseModel):
  email: EmailStr
  password: str

class UserIn(UserBase):
  id: int
