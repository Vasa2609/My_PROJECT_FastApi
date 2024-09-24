from . import schemas
from db.Note import Notes
from fastapi import Depends, HTTPException, status
from db.database import create_db
from sqlalchemy.orm import Session


def create_notes(db: Session, note: schemas.NoteCreate):
    db_note = Notes(
        title=note.title,
        name_author=note.name_author,
        content=note.content,
        image_url=note.image_url
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


def get_note(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Notes).offset(skip).limit(limit).all()


def get_note_by_id(db: Session, note_id: int):
    return db.query(Notes).filter(Notes.id == note_id).first()


def update_note(db: Session, note_id: int, note: schemas.NoteUpdate):
    db_note = db.query(Notes).filter(Notes.id == note_id).first()

    db_note.title = note.title
    db_note.content = note.content
    db_note.name_author = note.name_author
    db_note.image_url = note.image_url

    db.commit()
    db.refresh(db_note)

    return db_note


def delete_notes(db: Session, note_id: int):
    notes = db.query(Notes).filter(Notes.id == note_id).first()
    if notes:
        db.delete(notes)
        db.commit()
        return notes













