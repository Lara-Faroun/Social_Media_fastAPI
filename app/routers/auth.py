from fastapi import  HTTPException, Response,status,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import  get_db
from sqlalchemy.orm import Session
from .. import schemas,models, constants
from .. import utils, oauth2

router = APIRouter(tags=['authentication'])

@router.post('/login',response_model=schemas.Token)
async def login(user_credentials:OAuth2PasswordRequestForm = Depends() , db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=constants.INVALID_CREDENTIALS)
    
    if not utils.verify(user_credentials.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=constants.INVALID_CREDENTIALS)

    # create token 
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    #return token 
    return{'access_token' : access_token, 
           "token_type":"bearer"}