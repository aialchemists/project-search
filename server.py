import time

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from utils.configs import configs

app = FastAPI(title="Vector Search - APIs")

results = [
  {
    "text": "Myra was next to him, her ear to the ground, listening for the gallop of horses' hoofs. I got up and went over to them.",
    "file_path": "http://localhost:8000/files/data/The day's play.pdf",
    "score": 0.75
  },
  {
    "text": "I took the Queen Anne staircase on my—in the proper stalking position. I moved very slowly, searching for spoor. Half-way down the stairs my back fin slipped and I shot over the old oak at a tremendous pace, landing in the hall like a Channel swimmer. Looking up, I saw Thomas in front of me.",
    "file_path": "http://localhost:8000/files/data/The day's play.pdf",
    "score": 0.6
  },
  {
    "text": "Pars in gramineis exercent membra palæstris, Contendunt ludo, et fulvâ luctantur arenâ: Pars pedibus plaudunt choreas, et carmina dicunt.---- Arma procul, currusque virûm miratur inanes.",
    "file_path": "http://localhost:8000/files/data/The chase.txt",
    "score": 0.45
  }
]

@app.get("/", include_in_schema=False)
async def root_api():
    response = RedirectResponse(url='/docs')
    return response

@app.get("/api/configs")
async def configs_api():
    return configs

@app.get("/api/search")
async def search_api(query):
    return {
      "results": results
    }

@app.get("/files/{file_path}")
async def files_api(file_path):
    return {
      "file_path": file_path
    }
