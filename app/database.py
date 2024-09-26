from sqlmodel import SQLModel, Session
from app.models import Tender, Bid, BidReview, TenderHistory, BidHistory, BidDecisionRecord
from sqlmodel import create_engine

DB_HOST = "HOST"
DB_PORT = "PORT"
DB_NAME = "NAME"
DB_USER = "USER"
DB_PASSWORD = "PASSWORD"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DATABASE_URL += "?target_session_attrs=read-write"

engine = create_engine(DATABASE_URL)

JDBC_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}?targetServerType=primary"


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine, tables=[Tender.__table__, Bid.__table__,
                                                 BidReview.__table__, TenderHistory.__table__, BidHistory.__table__,
                                                 BidDecisionRecord.__table__])
