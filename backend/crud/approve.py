from sqlalchemy.orm import Session
from models.db import Activities, Notes
from schemas.notes import NoteCreate
from crud.types import AcceptState
from fastapi import HTTPException

def get_activity_by_id(db: Session, activity_id: int):
    activity = db.query(Activities).filter(Activities.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

def submit_activity_for_approval(db: Session, activity_id: int):
    activity = get_activity_by_id(db, activity_id)
    if activity.state == AcceptState.REQUESTED.value:
        raise HTTPException(status_code=400, detail="Activity is already waiting for approval")
    activity.state = AcceptState.REQUESTED.value
    db.commit()
    db.refresh(activity)
    return {"message": "Activity submitted for approval", "activity": activity}

def approve_activity(db: Session, activity_id: int, userid: int, note: str = None):
    activity = get_activity_by_id(db, activity_id)
    if activity.state != AcceptState.REQUESTED.value:
        raise HTTPException(status_code=400, detail="Activity must be in 'requested' state to approve")
    activity.state = AcceptState.APPROVED.value
    db.commit()
    db.refresh(activity)
    if note:
        create_note_for_activity(db, activity_id, NoteCreate(note=note, event_state=AcceptState.APPROVED, userid=userid))
    return {"message": "Activity approved", "activity": activity}

def super_approve_activity(db: Session, activity_id: int, userid: int, note: str = None):
    activity = get_activity_by_id(db, activity_id)
    if activity.state != AcceptState.APPROVED.value:
        raise HTTPException(status_code=400, detail="Activity must be 'approved' before super approval")
    activity.state = AcceptState.SUPER_APPROVED.value
    db.commit()
    db.refresh(activity)
    if note:
        create_note_for_activity(db, activity_id, NoteCreate(note=note, event_state=AcceptState.SUPER_APPROVED, userid=userid))
    return {"message": "Activity super approved", "activity": activity}

def reject_activity(db: Session, activity_id: int, userid: int, note: str = None):
    activity = get_activity_by_id(db, activity_id)
    if activity.state in [AcceptState.APPROVED.value, AcceptState.SUPER_APPROVED.value]:
        raise HTTPException(status_code=400, detail="Approved activities cannot be rejected")
    activity.state = AcceptState.DENIED.value
    db.commit()
    db.refresh(activity)
    if note:
        create_note_for_activity(db, activity_id, NoteCreate(note=note, event_state=AcceptState.DENIED, userid=userid))
    return {"message": "Activity rejected", "activity": activity}

def create_note_for_activity(db: Session, activity_id: int, note: NoteCreate):
    activity = get_activity_by_id(db, activity_id)
    db_note = Notes(
        note=note.note,
        event_state=note.event_state,
        activity_id=activity_id,
        userid=note.userid
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
