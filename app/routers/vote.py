from fastapi import  HTTPException, Response,status,Depends,APIRouter
import models, schemas , oauth2
from database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/votes",
    tags=['votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_for_post(voting:schemas.Vote, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post= db.query(models.Post).filter(models.Post.id == models.Vote.post_id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
    

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == voting.post_id and models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if voting.vote_dir == 1:

        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"current user {current_user.id} has already voted on {voting.post_id} post")

        else:
            new_vote = models.Vote(post_id = voting.post_id , user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return{"message":"successfully voted "}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"current user {current_user.id} hadn't voted on {voting.post_id} post before")
        
        vote_query.delete(synchronize_session = False)
        db.commit()
        return{"message":"successfully deleted vote "}


