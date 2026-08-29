import sys
import os
import asyncio
import time
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse  # <--- Added import

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "module1"))
sys.path.append(os.path.join(BASE_DIR, "module1", "src"))
sys.path.append(os.path.join(BASE_DIR, "module4"))

from market.market import Market
from index_engine import IndexEngine

app = FastAPI(title="AlgoClash Engine Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

market_instance = Market()
index_engine = IndexEngine()

market_data: Dict[str, float] = {}
price_history: Dict[str, List[float]] = {}

@app.on_event("startup")
async def startup_event():
    async def market_loop():
        while True:
            if hasattr(market_instance, "update"):
                market_instance.update()
                
            if hasattr(market_instance, "get_prices"):
                raw_prices = market_instance.get_prices()
                if isinstance(raw_prices, dict):
                    market_data.update(raw_prices)

            if hasattr(index_engine, "calculate"):
                indices = index_engine.calculate(market_data)
                if isinstance(indices, dict):
                    market_data.update(indices)
            elif hasattr(index_engine, "update"):
                indices = index_engine.update(market_data)
                if isinstance(indices, dict):
                    market_data.update(indices)

            for symbol, price in market_data.items():
                if symbol not in price_history:
                    price_history[symbol] = []
                price_history[symbol].append(price)

            await asyncio.sleep(3)

    asyncio.create_task(market_loop())

# --- SERVE DASHBOARD HTML AT ROOT ---
@app.get("/", response_class=FileResponse)
def serve_dashboard():
    return FileResponse("index.html")

# --- API ENDPOINTS ---
@app.get("/market/prices")
def get_prices():
    return {"timestamp": time.time(), "prices": market_data}

@app.get("/market/history/{symbol}")
def get_history(symbol: str):
    if symbol not in price_history:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return {"symbol": symbol, "history": price_history[symbol]}