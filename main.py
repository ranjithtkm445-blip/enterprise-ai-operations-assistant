# Patch must happen before any crewai submodule is imported
import crewai.llms.cache as _cache
_cache.mark_cache_breakpoint = lambda msg: msg  # type: ignore[assignment]

import litellm
litellm.drop_params = True

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from backend.crew import run_query
from backend.db.database import init_db
from backend.rag.vector_store import get_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    get_collection()
    yield


app = FastAPI(title="Enterprise AI Operations Assistant", lifespan=lifespan)


class ChatRequest(BaseModel):
    user: str
    message: str


class ChatResponse(BaseModel):
    user: str
    response: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    import traceback
    try:
        response = run_query(req.message)
        return ChatResponse(user=req.user, response=response)
    except Exception:
        traceback.print_exc()
        raise
