from fastapi import FastAPI
from starlette.responses import RedirectResponse

from utils.configs import configs

app = FastAPI(title="Vector Search - APIs")

@app.get("/", include_in_schema=False)
async def root_api():
    response = RedirectResponse(url='/docs')
    return response

@app.get("/api/configs")
async def configs_api():
    return configs
