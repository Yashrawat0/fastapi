from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.vote, db: Session = Depends(database.get_db), 
         current_user:int = Depends(oauth.get_current_user)):
    
    """this function is providing the clients to vote on the post. so To vote 
    the client have to pass post_id and dir(In which client can passed two values 1 and 0) 
    1 => to vote or like and 
    0 => To remove the like or vote from the post)
    """

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()    # check if the post really exist in the database to be like.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()    # check if voter have already like a post or not 

    if (vote.dir == 1): # if voter has pass 1
        if found_vote:     # (if yes than voter can not vote again on the same post) 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already votes on post {vote.post_id}")
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)   # (if no he can vote...)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    
    else:  # if voter has pass 0 means he like to remove the vote from the post  
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
    
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}



        
