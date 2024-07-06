from .. import models, utils, schemas
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """creating a new user new user register on the app by taking his email_id and password and also password
      is not store in the database just in the raw form but the password is hashed one then they are stored 
      in the Database in the hashed form"""

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
            # {**post.model_dump()} => here we are unpacking the dict
    
    
    db.add(new_user)   # send newly created post to the database
    db.commit()   # committing changes in database
    db.refresh(new_user)   # it will return the newly created post from the database

    return new_user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:   # (common for both the methods)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= {"message": f"user with id: {id} was not found"})
    
    return user

