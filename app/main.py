from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from typing import Union
from pydantic import BaseModel
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

URL = "https://631982548e51a64d2be5dca5.mockapi.io/users"

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


class Track(BaseModel):
    role: str
    instruments: list[str]
    is_primary: bool

class Request(BaseModel):
    genre: str
    bpm : list[int]
    keys : list[str]
    time_signatures: str
    tracks: Union[list[Track], None] = None


@app.post("/test")
async def test(request: Request):
    print(request)
    return "성공"


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/api_test/")
async def call_other_api() : 
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        data = response.json()
        arr = []
        for i in range(len(data)):
            if data[i]['name'] == "Lila Bahringer":
                arr.append(data[i])
        if arr == []:
            raise HTTPException(status_code=400, detail="존재하지 않는 데이터 입니다.")
        return arr


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: schemas.TypeTest, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,

        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.post("/type_test/")
async def type_test(input:schemas.TypeTest) -> int:

    return {"input": input}






@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

