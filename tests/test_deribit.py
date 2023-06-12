import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from deribit_APS import DeribitClient

import pytest
from deribit_APS import DeribitClient

@pytest.mark.asyncio
async def test_fetch_price_valid_ticker():
    # This test checks that the fetch_price method returns a float when given a valid ticker.
    client = DeribitClient()
    btc_price = await client.fetch_price("BTC-PERPETUAL")
    eth_price = await client.fetch_price("ETH-PERPETUAL")

    assert isinstance(btc_price, float)
    assert isinstance(eth_price, float)

@pytest.mark.asyncio
async def test_fetch_price_invalid_ticker():
    # This test checks that the fetch_price method returns None or raises an exception when given an invalid ticker.
    client = DeribitClient()
    try:
        price = await client.fetch_price("INVALID-TICKER")
        assert price is None
    except Exception:
        pass  # An exception is expected here, so we just pass.

@pytest.mark.asyncio
async def test_fetch_price_network_error():
    # This test checks that the fetch_price method raises an exception when there is a network error.
    # To simulate a network error, we give an invalid base URL to the DeribitClient.
    client = DeribitClient()
    client.BASE_URL = "http://invalid-url"
    with pytest.raises(Exception):
        await client.fetch_price("BTC-PERPETUAL")

