from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "postgresql+asyncpg://iam:98@localhost/mytestovoe"

# Initialize SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Define the model
Base = declarative_base()

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    price = Column(Float)
    timestamp = Column(Integer)

