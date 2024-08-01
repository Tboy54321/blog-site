from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class blogs(Base):

  __tablename__ = "blogs"

  id = Column(Integer, primary_key=True)
  title = Column(String, index=True)
  description = Column(String, index=True)