from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Activity, Note
from database import get_db
from schemas import NoteCreate
from crud.dependencies import AcceptState

app = FastAPI()

@app.post("/activities/{activity_id}/submit_for_approval")
def submit_for_approval(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    if activity.state != AcceptState.REQUESTED.value:
        activity.state = AcceptState.REQUESTED.value  
        db.commit()
        db.refresh(activity)
        return {"message": "Activity submitted for approval", "activity": activity}
    
    raise HTTPException(status_code=400, detail="Activity is already waiting for approval")


@app.post("/activities/{activity_id}/approve")
def approve_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    if activity.state != AcceptState.REQUESTED.value:
        raise HTTPException(status_code=400, detail="Activity must be in 'requested' state to approve")
    
    activity.state = AcceptState.APPROVED.value  
    db.commit()
    db.refresh(activity)
    return {"message": "Activity approved", "activity": activity}


@app.post("/activities/{activity_id}/super_approve")
def super_approve_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    if activity.state != AcceptState.APPROVED.value:
        raise HTTPException(status_code=400, detail="Activity must be 'approved' before super approval")
    
    activity.state = AcceptState.SUPER_APPROVED.value  
    db.commit()
    db.refresh(activity)
    return {"message": "Activity super approved", "activity": activity}


@app.post("/activities/{activity_id}/reject")
def reject_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    if activity.state in [AcceptState.APPROVED.value, AcceptState.SUPER_APPROVED.value]:
        raise HTTPException(status_code=400, detail="Approved activities cannot be rejected")

    activity.state = AcceptState.DENIED.value  
    db.commit()
    db.refresh(activity)
    return {"message": "Activity rejected", "activity": activity}


@app.post("/activities/{activity_id}/notes")
def create_note_for_activity(activity_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    db_note = Note(**note.dict(), activity_id=activity_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
