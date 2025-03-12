from fastapi import  HTTPException, Response,status,Depends,APIRouter
from .. import models, schemas , oauth2 ,  constants
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote_for_post(voting:schemas.Vote, db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post= db.query(models.Post).filter(models.Post.id == voting.post_id).first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=constants.POST_NOT_FOUND.format(voting.post_id))
    
    vote_query = db.query(models.Vote).filter((models.Vote.post_id == voting.post_id) and (models.Vote.user_id == current_user.id))
    found_vote = vote_query.first()
    if voting.vote_dir == 1:

        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=constants.VOTE_ALREADY_EXISTS.format(current_user.id, voting.post_id))

        else:
            new_vote = models.Vote(post_id = voting.post_id , user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return{"message": constants.VOTE_ADDED}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=constants.VOTE_NOT_FOUND.format(current_user.id, voting.post_id))
        
        vote_query.delete(synchronize_session = False)
        db.commit()
        return{"message":constants.VOTE_DELETED}


