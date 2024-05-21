from sqlalchemy.orm import Session

from . import models, schemas


def get_work(db: Session, work_id: int):
    return db.query(models.Work).filter(models.Work.id == work_id).first()


def get_works(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Work).offset(skip).limit(limit).all()


def create_work(db: Session, work: schemas.WorkCreate):
    db_work = models.Work(
        name=work.name,
        tree_id=work.tree_id,
        start_date=work.start_date,
        end_date=work.end_date
    )
    if work.parent_id != '':
        db_work.parent_id = work.parent_id
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


def update_work(db: Session, work: schemas.Work):
    db_work = db.query(models.Work).filter(models.Work.id == work.id).one_or_none()
    if db_work is None:
        return None
    for var, value in vars(work).items():
        if var == 'parent_id': 
            continue
        setattr(db_work, var, value) if value else None

    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work
