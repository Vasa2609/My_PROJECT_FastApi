from sqlalchemy import Column, Integer, String, Text
from db.database import Base


class Notes(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    name_author = Column(String, nullable=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String, nullable=False)
