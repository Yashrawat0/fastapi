from .. import models, utils, schemas, oauth
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(tags=["authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ this function is providing user to {login} to the app and providing the (token no.)"""
    
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:   # (common for both the methods)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= {"message": f"user with email: {user_credentials.email} was not found"})
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    

    access_token = oauth.create_access_token(data = {"user_id": user.id})\
    
    return {"access_token": access_token, 
            "token_type": "bearer"}

    
    


    



