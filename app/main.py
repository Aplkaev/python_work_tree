from fastapi import Depends, FastAPI, Path
from sqlalchemy.orm import Session
from uuid import UUID

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


@app.get("/work", response_model=list[schemas.Work])
async def get_works(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)):
    works = crud.get_works(db=db)
    return works


@app.get("/work/tree/{id}", response_model=list[schemas.Work])
async def get_work_for_tree(
        id: int = Path(title="The ID of the item to get tree"),
        db: Session = Depends(get_db)):
    works = crud.get_works_for_tree(db=db, tree_id=id)
    return works


@app.get("/work/{id}", response_model=schemas.Work)
async def get_work(
        id: UUID = Path(title="The ID of the item to get work"),
        db: Session = Depends(get_db)):
    works = crud.get_works(db=db)
    return works


@app.post("/work", response_model=schemas.Work)
async def create_work(work: schemas.WorkCreate, db: Session = Depends(get_db)):
    return crud.create_work(db=db, work=work)


@app.put("/work", response_model=schemas.Work)
async def update_work(work: schemas.Work, db: Session = Depends(get_db)):
    return crud.update_work(db=db, work=work)
