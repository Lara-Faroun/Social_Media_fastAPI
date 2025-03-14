from typing import List, Optional
from fastapi import  HTTPException, Response,status,Depends,APIRouter
from .. import models, schemas , oauth2 ,constants
from ..database import  get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.get("/",response_model= List[schemas.PostOut])
async def get_posts(db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user),
                    limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()    

    ###Only Retrieving Logged in User's###
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
   
   ###Rrtrieving all posts###
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
    isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts 

@router.post("/",status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
async def createpost(post:schemas.PostCreate,db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) 
    # VALUES (%s , %s, %s) RETURNING *""", (post.title , post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.get("/posts/latest")
# def get_latest():
#     latest = my_posts[len(my_posts)-1]
#     return{"latest_post":latest}

@router.get("/{id}",response_model=schemas.PostOut)
async def get_post(id :int, db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
    isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= constants.POST_NOT_FOUND.format(id))
    return post

@router.delete("/{id}")
async def delete_post(id:int, db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first() 
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=constants.POST_NOT_FOUND.format(id))

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=constants.NOT_AUTHORIZED)
    
    post_query.delete(synchronize_session = False)
    db.commit()
    
    return Response( status_code = status.HTTP_204_NO_CONTENT )

@router.put("/{id}",response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=%s,content=%s,published=%s WHERE id = %s
    # RETURNING *""",
    # (post.title , post.content, post.published, str(id),))
    
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()


    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=constants.POST_NOT_FOUND.format(id))
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=constants.NOT_AUTHORIZED)
    
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first()
