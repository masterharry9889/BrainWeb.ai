from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import routes

from contextlib import asynccontextmanager
from .database import init_db

import asyncio
from .services.graph_writer import run_graph_writer

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    task = asyncio.create_task(run_graph_writer())
    yield
    task.cancel()

app = FastAPI(title="INGOT.ai Backend", version="1.0.0", lifespan=lifespan)

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
