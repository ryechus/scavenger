import datetime
import uuid

from pytz import timezone
from sqlmodel import Field, Session, SQLModel, create_engine, select


def generate_uuid(*args, **kwargs):
    return str(uuid.uuid4())


def make_datetime(*args, **kwargs):
    tz = timezone("UTC")
    now = datetime.datetime.now(tz=tz)
    return now


class Auction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True)
    name: str
    starting_datetime: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False)
    ending_datetime: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False)
    starting_price: int
    current_bid: int | None = None
    is_deleted: bool = Field(default=False)


class Bid(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=generate_uuid, primary_key=True)
    bid_amount: int
    max_bid_amount: int = Field(nullable=True)
    client_timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False)
    created_at: datetime.datetime = Field(default_factory=make_datetime, nullable=False)
    customer_id: uuid.UUID = Field(default=None, index=True)
    auction_id: uuid.UUID = Field(nullable=False, foreign_key="auction.id")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
