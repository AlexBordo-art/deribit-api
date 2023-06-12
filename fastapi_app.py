from fastapi import FastAPI
from sqlalchemy.future import select
from typing import List
from dataclasses import dataclass
from datetime import datetime
from models import Price, async_session

@dataclass
class PriceData:
    symbol: str
    price: float
    timestamp: int

app = FastAPI()

@app.get("/prices/{ticker}", response_model=List[PriceData])
async def get_prices(ticker: str):
    async with async_session() as session:
        result = await session.execute(select(Price).where(Price.symbol == ticker))
        prices = result.scalars().all()
        return [PriceData(symbol=price.symbol, price=price.price, timestamp=price.timestamp) for price in prices]

@app.get("/price/{ticker}/latest", response_model=PriceData)
async def get_latest_price(ticker: str):
    async with async_session() as session:
        result = await session.execute(
            select(Price).where(Price.symbol == ticker).order_by(Price.timestamp.desc())
        )
        price = result.scalars().first()
        return PriceData(symbol=price.symbol, price=price.price, timestamp=price.timestamp) if price else None

@app.get("/price/{ticker}/date", response_model=List[PriceData])
async def get_price_by_date(ticker: str, date: str):
    timestamp_start = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
    timestamp_end = timestamp_start + 24 * 60 * 60

    async with async_session() as session:
        result = await session.execute(
            select(Price)
            .where(Price.symbol == ticker, Price.timestamp >= timestamp_start, Price.timestamp < timestamp_end)
        )
        prices = result.scalars().all()
        return [PriceData(symbol=price.symbol, price=price.price, timestamp=price.timestamp) for price in prices]

