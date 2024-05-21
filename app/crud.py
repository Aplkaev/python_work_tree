from sqlalchemy.orm import Session
from uuid import UUID
from pytz import timezone

from . import models, schemas


def get_work(db: Session, work_id: UUID):
    work = db.query(models.Work).filter(
        models.Work.id == work_id).first()
    return 'None'


def get_works(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Work).offset(skip).limit(limit).all()


def get_works_for_tree(db: Session, tree_id: int):
    return db.query(models.Work).filter(
        models.Work.tree_id == tree_id,
        not models.Work.is_deleted).all()


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

    update_date_work(db, db_work)
    db.commit()

    return db_work


def update_work(db: Session, work: schemas.Work):
    db_work = db.query(models.Work).filter(
        models.Work.id == work.id,
        not models.Work.is_deleted,
        models.Work.tree_id == work.tree_id).one_or_none()
    if db_work is None:
        return None
    for var, value in vars(work).items():
        # не обновляем родителя
        if var == 'parent_id':
            continue
        setattr(db_work, var, value) if value else None

    update_date_work(db, db_work)

    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


def update_date_work(db: Session, db_work: models.Work):
    limit_date = get_date_limit_children(db, db_work)
    if db_work.start_date.replace(tzinfo=timezone('UTC')) \
            > limit_date['start_date'].replace(tzinfo=timezone('UTC')):
        '''
        ошибка дат, родитель не может принимать
        дату больше чем limit_date['start_date]
        '''
        return

    if db_work.end_date.replace(tzinfo=timezone('UTC')) \
            < limit_date['end_date'].replace(tzinfo=timezone('UTC')):
        '''
        ошибка дат, родитель не может принимать
        дату меньше чем limit_date['end_date]
        '''
        return

    if db_work.parent_id is not None:
        parent_work = get_first_parent(db, db_work)
        update_all_tree(db, parent_work)


def update_all_tree(db: Session, work: models.Work):
    """
    Обновляем даты работ, с самого нижнего элемента
    """
    limit_date = get_date_limit_children(db, work)
    work.start_date = limit_date['start_date']
    work.end_date = limit_date['end_date']
    db.add(work)

    db_works = db.query(models.Work).filter(
        models.Work.parent_id == work.id,
        not models.Work.is_deleted,
        models.Work.tree_id == work.tree_id).all()
    if not db_works:
        return
    for db_work in db_works:
        update_all_tree(db, db_work)


def get_first_parent(db: Session, work: models.Work):
    """
    получаем первого родителя
    """
    if work.parent_id is None:
        return work
    db_work = db.query(models.Work).filter(
        models.Work.id == work.parent_id,
        not models.Work.is_deleted,
        models.Work.tree_id == work.tree_id).one_or_none()
    if db_work is None:
        return work
    return get_first_parent(db, db_work)


def get_date_limit_children(db: Session, work: models.Work):
    """
    получаем минимальное дат работ с дочерних работ
    """
    db_works = db.query(models.Work).filter(
        models.Work.parent_id == work.id,
        not models.Work.is_deleted,
        models.Work.tree_id == work.tree_id).all()
    if not db_works:
        return {
            'start_date': work.start_date,
            'end_date': work.end_date
        }
    for db_work in db_works:

        limit_date = get_date_limit_children(db, db_work)
        if limit_date['start_date'].replace(tzinfo=timezone('UTC')) \
                > db_work.start_date.replace(tzinfo=timezone('UTC')):
            limit_date['start_date'] = db_work.start_date

        if limit_date['end_date'].replace(tzinfo=timezone('UTC')) \
                < db_work.end_date.replace(tzinfo=timezone('UTC')):
            limit_date['end_date'] = db_work.end_date

    return limit_date
