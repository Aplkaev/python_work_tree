from fastapi import Depends, FastAPI, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def get_interval():
    return {
        'message': 'hello'
    }


@app.post("/work", response_model=schemas.Work)
async def create_work(work: schemas.WorkCreate, db: Session = Depends(get_db)):
    return crud.create_work(db=db, work=work)

@app.put("/work", response_model=schemas.Work)
async def update_work(work: schemas.Work, db: Session = Depends(get_db)):
    return crud.update_work(db=db, work=work)
    

# alembic init migration
# alembic revision --autogenerate -m 'initial'
# alembic upgrade head