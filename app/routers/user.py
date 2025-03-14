from fastapi import HTTPException,status,Depends, APIRouter
from .. import models , schemas , constants
from ..database import  get_db
from ..utils import hash
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
async def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    
    #hash user.password
    user.password = hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
async def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=constants.USER_NOT_FOUND.format(id)
        )
    
    return user
