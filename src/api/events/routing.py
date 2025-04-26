import os

from fastapi import APIRouter, Depends, HTTPException
from .models import EventModel, EventListSchema, EventCreateSchema, EventUpdateSchema, get_utc_now
from api.db.session import get_session
from sqlmodel import Session, select

router = APIRouter()

from ..db.config import DATABASE_URL

@router.get("/", response_model = EventListSchema)
def read_events(session: Session = Depends(get_session)):
    #query = select(EventModel).limit(2)
    #query = select(EventModel).order_by(EventModel.id.desc())
    query = select(EventModel).order_by(EventModel.id.desc()).limit(2)
    results = session.exec(query).all()

    return {
        "results" : results,
        "count": len(results)
    }

#Send data hhers
@router.post("/", response_model=EventModel)
def create_event(
    payload: EventCreateSchema, 
    session: Session = Depends(get_session)
    ):
    data = payload.model_dump()
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


#Retrive a particulr quesry

@router.get("/{event_id}", response_model= EventModel)
def get_event(event_id : int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()

    if not result:
        raise HTTPException(status_code = 404, detail = "Event not fpund")
    return result

@router.put("/{event_id}", response_model= EventModel)
def update_event(
    event_id: int, 
    payload: EventUpdateSchema,
    session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code= 404,details = "Not found")
    data = payload.model_dump()
    for k, v in data.items():
        setattr(obj, k, v)

    #Adding updated at attribute
    obj.updated_at = get_utc_now()

    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
