from fastapi import FastAPI
from utils.configs import configs

app = FastAPI()

@app.get("/")
async def root_api():
    return {
        "service": "Vector Search"
    }

@app.get("/api/configs")
async def configs_api():
    return configs
