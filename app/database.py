from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERECT_FILE = os.path.join(BASE_DIR, 'serects.json')
serects = json.loads(open(SERECT_FILE).read())
DB = serects["DB"]

DB_URL = f"mysql+pymysql://{DB['user']}:{DB['password']}@{DB['host']}/{DB['database']}?charset=utf8"

engine = create_engine(
    DB_URL, encoding = 'utf-8'
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
