from fastapi import FastAPI
from .database import engine
from .routers import post, user, authentication, vote
from . import config, models
from .database import get_db
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)   # it will go to the (post) file and find all the router and treat if as @app.
app.include_router(user.router) 
app.include_router(authentication.router)    
app.include_router(vote.router)

@app.get("/")  
async def root():
    return {"message": "successful"}
    

