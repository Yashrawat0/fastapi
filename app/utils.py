from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")    # here we are just telling that we are using (bcryt) algorithm to hashing the password.

def hash(password: str):
    return  pwd_context.hash(password)   # hash the password - user.password



def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)