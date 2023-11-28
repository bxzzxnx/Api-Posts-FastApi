from fastapi import Depends, HTTPException, APIRouter


from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    tags=['Vote'],
    prefix='/vote'
)


@router.post('/', status_code=201)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail='Post not found')

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.author_id == current_user.id)

    found_vote = vote_query.first()

    if vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=409, detail=f'User {current_user.id} ja votou no post {vote.post_id}')

        add_vote = models.Vote(
            author_id=current_user.id,
            post_id=vote.post_id
        )

        db.add(add_vote)
        db.commit()
        return {'message': 'Successfully voted'}

    if not found_vote:
        raise HTTPException(status_code=409, detail='Voto não existe')

    vote_query.delete(synchronize_session=False)
    db.commit()
    return {'message': 'Voto deletado'}


@router.get('/')
def get_all_votes(db: Session = Depends(get_db)):
    teste = db.query(models.Vote).all()
    return teste


@router.get('/post/{post_id}')
def get_number_of_likes_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail='Post não existe')
    query = db.query(models.Vote).filter(
        models.Vote.post_id == post_id).count()
    return {'Number of likes': query}
