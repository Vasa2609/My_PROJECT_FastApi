from pydantic import BaseModel
from typing import List
from fastapi import Form
from typing import Optional

class NoteBase(BaseModel):
    title: str = Form(...)
    name_author: str = Form(...)
    content: str = Form(...)
    image_url: Optional[str] = None


class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    image_url: Optional[str] = None


class NoteRead(NoteBase):
    id: int
    title: str = Form(...)
    name_author: str = Form(...)
    content: str = Form(...)
    image_url: Optional[str] = None


    class Config:
        from_attributes = True



