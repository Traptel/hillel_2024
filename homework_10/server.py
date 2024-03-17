import time

import httpx
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    currency_from: str
    currency_to: str


app = FastAPI()
cache = {}


@app.post("/items/")
async def get_current_market_state(item: Item):
    currency_from = item.currency_from
    currency_to = item.currency_to

    cached_response = cache.get(currency_from, {}).get(currency_to)
    if cached_response is not None:
        if time.time() - cached_response["timestamp"] < 10:
            return {"exchange_rate": cached_response["value"], "cached": True}

    api_key = "V2V43QAQ8RILGBOW"
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_from}&to_currency={currency_to}&apikey={api_key}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        data = response.json()["Realtime Currency Exchange Rate"]
        rate = data.get("5. Exchange Rate")

        if currency_from not in cache:
            cache[currency_from] = {}
        cache[currency_from][currency_to] = {
            "value": rate,
            "timestamp": time.time(),
        }
        return {"exchange_rate": rate, "cached": False}
    else:
        raise Exception(
            f"Failed to get the exchange rate."
            f"Status code: {response.status_code}"
        )
