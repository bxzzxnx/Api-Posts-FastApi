from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credential.username).first()
    if user == None:
        raise HTTPException(status_code=403, detail='Invalid')

    user_permited = utils.verify_password(
        user_credential.password, user.password)
    if not user_permited:
        raise HTTPException(status_code=403, detail='Invalid')

    access_token = oauth2.create_access_token(
        data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
