from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.model.model import Wishes
from app.schema.schema import patch_schema, wish_schema
from app.session.session import create_get_session

router = APIRouter()


@router.get("/api/wishes", response_model=List[wish_schema], status_code=200)
async def read_wishes(db: Session = Depends(create_get_session)):
    wishes = db.query(Wishes).all()
    return wishes


@router.post("/api/wishes", response_model=wish_schema, status_code=201)
async def add_wish(wish: wish_schema, db: Session = Depends(create_get_session)):
    new_wish = Wishes(
        person=wish.person,
        item=wish.item,
        link=wish.link,
        purchased=wish.purchased,
        purchased_by=wish.purchased_by,
        date_added=wish.date_added,
    )
    db.add(new_wish)
    db.commit()

    return new_wish


@router.get("/api/wishes/{id}", response_model=wish_schema, status_code=200)
async def get_wish(id: int, db: Session = Depends(create_get_session)):
    wish = db.query(Wishes).get(id)
    return wish


@router.patch("/api/wishes/{id}", response_model=wish_schema, status_code=200)
async def update_wish(
    id: int, patch: patch_schema, db: Session = Depends(create_get_session)
):
    db_wish = db.query(Wishes).get(id)
    db_wish.purchased = patch.purchased
    db_wish.purchased_by = patch.purchased_by
    db.commit()
    db.refresh(db_wish)

    return db_wish


@router.delete("/api/wishes/{id}", status_code=200)
async def delete_wish(id: int, db: Session = Depends(create_get_session)):
    db_wish = db.query(Wishes).get(id)
    if not db_wish:
        raise HTTPException(status_code="404", detail="Wish id does not exist")

    db.delete(db_wish)
    db.commit()

    return None
