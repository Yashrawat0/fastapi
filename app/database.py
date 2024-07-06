from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor    # this is to get column name in return with row when some query is executed.
import psycopg2
import time
from .config import settings

# ______________________________________________________________________ (not using this method) (first method)
# while True:
#     try: 
#         # connecting to the database
#         conn = psycopg2.connect(host="localhost", database="fastapi", 
#                                 user="postgres", password="password", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection was successful")
#         break

#     except Exception as error:   
#         print("connecting to database failed")
#         print("error: ", error )
#         time.sleep(2)



# my_post = [{"title": "title of the post 1", "content": "content of post 1", "id": 1}, # just for practice
#            {"title": "my name is Yash Rawat", "content": "I like pizza", "id": 2}] 


# def find_post(id):
#       for post in my_post:
#         if post["id"] == id:
#              return post
        
# def find_index_post(id):
#     for i, post in enumerate(my_post):
#         if post["id"] == id:
#             return i
# _______________________________________________________________________________


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
    
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()