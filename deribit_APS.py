import aiohttp
import asyncio
import time
from models import Price, async_session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "postgresql+asyncpg://iam:***@localhost/mytestovoe"

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

# Deribit client
class DeribitClient:
    BASE_URL = "https://www.deribit.com/api/v2/public/ticker"

    async def fetch_price(self, symbol: str):
        async with aiohttp.ClientSession() as session:
            params = {"instrument_name": symbol}
            async with session.get(self.BASE_URL, params=params) as response:
                data = await response.json()
                return data["result"]["last_price"]

# Fetch prices and save to database
async def fetch_prices():
    client = DeribitClient()
    btc_price = await client.fetch_price("BTC-PERPETUAL")
    eth_price = await client.fetch_price("ETH-PERPETUAL")

    async with async_session.begin() as session:
        session.add_all([
            Price(symbol="BTC-PERPETUAL", price=btc_price, timestamp=int(time.time())),
            Price(symbol="ETH-PERPETUAL", price=eth_price, timestamp=int(time.time()))
        ])

# Create tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Main function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    scheduler = AsyncIOScheduler()

    # Create tables and fetch prices immediately
    loop.run_until_complete(asyncio.gather(create_tables(), fetch_prices()))

    # Then fetch prices every minute
    scheduler.add_job(fetch_prices, 'interval', minutes=1)
    scheduler.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.shutdown()

