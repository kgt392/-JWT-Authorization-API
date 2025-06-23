from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import Annotated
import models
from database import engine, SessionLocal
from pydantic import BaseModel
import auth
from auth import get_current_user

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"User": user}
