from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Role, Activity, Note  
from database import get_db

app = FastAPI()

@app.post("/activities/{activity_id}/approval")
def approve_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity.approved = True
    db.commit()
    return activity