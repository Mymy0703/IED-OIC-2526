from fastapi import FastAPI
from mongita import MongitaClientDisk
from pydantic import BaseModel
import json

class Musique(BaseModel):
    artiste: str
    genre: str
    titre: str
    url: str
    id: int


app = FastAPI()

with open("playlist.json", "r", encoding="utf-8") as f:
    ma_playlist = json.load(f)

@app.get("/")
def recuperer_playlist():
    return ma_playlist

@app.post("/")
def rajouter_musique(musique : Musique):
    ma_playlist.append(musique.dict())
    return ma_playlist

