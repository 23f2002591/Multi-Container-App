import os
import redis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True,
)

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/healthz")
def healthz():
    try:
        redis_client.ping()
        return {
            "status": "ok",
            "redis": "up"
        }
    except Exception:
        return {
            "status": "error",
            "redis": "down"
        }

@app.post("/hit/{key}")
def hit(key: str):
    count = redis_client.incr(key)
    return {
        "key": key,
        "count": count
    }

@app.get("/count/{key}")
def count(key: str):
    value = redis_client.get(key)

    return {
        "key": key,
        "count": int(value) if value else 0
    }
