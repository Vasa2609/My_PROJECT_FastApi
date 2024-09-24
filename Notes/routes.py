import uvicorn
import shutil
from . import crud, schemas
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from db.database import create_db
from fastapi.responses import JSONResponse
from typing import List, Optional

create_db()

app = FastAPI()


@app.post("/notes", response_model=schemas.NoteRead)
async def create_note(
    name_author: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    image_url: UploadFile = File(None),
    db: Session = Depends(create_db),
):

    image_path = None
    if image_url:
        image_path = f"images/{image_url.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image_url.file, buffer)


    new_note = schemas.NoteCreate(
        name_author=name_author,
        title=title,
        content=content,
        image_url=image_path if image_url else None
    )
    return crud.create_notes(db, new_note)


@app.put('/update_note{note_id}', response_model=schemas.NoteRead)
async def update_note(
        note_id: int,
        title: str = Form(...),
        content: str = Form(...),
        name_author: str = Form(...),
        image_url: UploadFile = File(None),
        db: Session = Depends(create_db)
):
    db_note = crud.get_note_by_id(db, note_id)
    if not db_note:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="Note not found")

    if image_url:
        image_path = f"images/{image_url.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image_url.file, buffer)
        db_note.image_url = image_path


    db_note.title = title
    db_note.content = content
    db_note.name_author = name_author

    db.commit()
    db.refresh(db_note)
    return crud.update_note(db, note_id, db_note)








@app.get('/notes/', response_model=List[schemas.NoteRead])
async def read_notes(db: Session = Depends(create_db), skip: int = 0, limit: int = 10):
    notes = crud.get_note(db, skip=skip, limit=limit)
    return notes


@app.get('/notes/{note_id}', response_model=schemas.NoteRead)
async def read_note(note_id: int, db: Session = Depends(create_db)):
    note = crud.get_note_by_id(db, note_id)
    if note is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Notes not found')
    return note


@app.delete('/delete_notes/{notes_id}', response_model=schemas.NoteRead)
async def delete_notes(note_id: int, db: Session = Depends(create_db)):
    note = crud.delete_notes(db, note_id)
    if note is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Notes not found')
    return note



