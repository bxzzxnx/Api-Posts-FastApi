from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict

from fastapi.responses import JSONResponse

from .. import schemas, models, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/', response_model=List[schemas.PostOut])
def get_all_posts(skip: int = 0, limit: int = 100, search: Optional[str] = '',  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(
        models.Vote, models.Vote.post_id == models.Post.id).group_by(
            models.Post.id).filter(
                models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get('/{id}', response_model=schemas.PostOut)
def get_post_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).outerjoin(
        models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=404, detail='Não encontrado')
    # if post.author_id != current_user.id:
    #     raise HTTPException(
    #         status_code=403, detail='Sem autorização para ver esse post')
    return post


@router.post('/', status_code=201, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(post.model_dump())

    print(current_user.id)
    new_post = models.Post(**post.model_dump(), author_id=current_user.id)

    # print(current_user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/{id}', status_code=204)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {id} does not exist')

    # print(post.author_id)
    # print(current_user.id)
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail='Sem autorização')
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=404, detail='Post não existe')
    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail='Sem autorização')
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
