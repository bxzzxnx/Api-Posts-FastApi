from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)


@router.get('/', response_model=List[schemas.UserPublic])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post('/', status_code=201, response_model=schemas.UserPublic)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    ''' Create a user '''

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserPublic)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(
            status_code=404, detail=f'User with id {id} not exists')
    return user


@router.post('/reset')
def reset_password(user: schemas.ChangePassword, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    is_user = utils.verify_password(user.password, current_user.password)
    if is_user == False:
        raise HTTPException(status_code=404, detail='Senha errada')
    new_password = utils.hash(user.new_password)
    current_user.password = new_password
    db.commit()
    return {'Message': 'Password changed successfully'}
