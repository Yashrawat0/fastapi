from .. import models, utils, schemas, oauth
from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)  # prefix is just to reduce the code since we are always going to start the url with /posts 


# user_id: int = Depends(oauth.get_current_user) this line is every function is checking if the user is loge-in or not..


# to get all the post from the database in the go.
@router.get("/", response_model=List[schemas.PostWithVoteResponse])  # we do not need to add /posts since it is already added to the router
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional [str] = ""):
    """to get all the post from the database in the go.
    (limit Parameter) is limiting the number of post you give when client request all post.
    """
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # if in future you want to implement that the login user get his post only when he request all posts and will not get other's user's posts (below line)
    # # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                        isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()






    #_____________________________________________
    # cursor.execute("SELECT * FROM post")
    # posts = cursor.fetchall()   # executing above query
    # print(posts)
    #_____________________________________________

    return results



# to create the post.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createposts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth.get_current_user)):   # validating the content sended by the user

    # print(post.model_dump()) # and this is a dict make by pydantic model (for practice)
    # print(post)  # this is a pydantic model  (for practice)

    # post_dict = post.model_dump()
    # post_dict["id"] = randint(0, 1000000)
    # my_post.append(post_dict)
    # return {"data": post_dict}
    # ____________________________________________________________________________________


    # ____________________________________________________________________________________
    # database query from (psycopg2)   - (one way to do it.)
    # cursor.execute("""INSERT INTO post (title, content, published) VALUES(%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published)) 
    # new_post = cursor.fetchone()
    # conn.commit()           # committing the changing in the database
    # return {"data": new_post}
    #___________________________________________________________________________________


    #___________________________________________________________________________________
    # this is most efficient way of interacting with database = use sqlalchemy  - ( second way of doing it.)
    print(current_user.id)
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
            # {**post.model_dump()} => here we are unpacking the dict
    

    db.add(new_post)   # send newly created post to the database
    db.commit()   # committing changes in database
    db.refresh(new_post)   # it will return the newly created post from the database

    return new_post


    


# to just get one post by passing the (id) in url.
@router.get("/{id}", response_model=schemas.PostWithVoteResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth.get_current_user)):   # validating that the frontend as only input the id and not any thing else. (id: int)
    
    #___________________________________________________________________________________
    # cursor.execute("SELECT * FROM post WHERE id = %s", (str(id),))   # (do not remove this , from query)
    # post = cursor.fetchone()
    # print(post)   # (for practice)
    #___________________________________________________________________________________


    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, 
                                        isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)   # (for practice)

    if not post:   # common for both the methods
        # response.status_code = status.HTTP_404_NOT_FOUND  # this line raises status code if (id) do not exit in our database
        # return {"message": f"post with id: {id} was not found"}

        # better way to raise a exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= {"message": f"post with id: {id} was not found"})
    
     
       
    return post
    

    

# deleting the post from database
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):

    #___________________________________________________________________________________
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    #___________________________________________________________________________________

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(post)   # (for practice)
    if post == None:
        # response.status_code = status.HTTP_404_NOT_FOUND  # this line raises status code if (id) do not exit in our database
        # return {"message": f"post with id: {id} was not found"}

        # better way to raise a exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= {"message": f"post with id: {id} was not found"})
    
    if post.user_id != current_user.id:   # check if the user is deleting his post only and not other's.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)   # deleting the post
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth.get_current_user)):

    #___________________________________________________________________________________
    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                 (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    #___________________________________________________________________________________

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        # response.status_code = status.HTTP_404_NOT_FOUND  # this line raises status code if (id) do not exit in our database
        # return {"message": f"post with id: {id} was not found"}

        # better way to raise a exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= {"message": f"post with id: {id} was not found"})
    
    if post.user_id != current_user.id:   # check if the user is updating his post only and not other's.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()