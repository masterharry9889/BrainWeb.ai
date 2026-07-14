from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import routes

from contextlib import asynccontextmanager
from .database import init_db, engine

import asyncio
from .services.graph_writer import run_graph_writer

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    task = asyncio.create_task(run_graph_writer())
    yield
    task.cancel()
    await engine.dispose()

app = FastAPI(title="BrainWeb.ai Backend", version="1.0.0", lifespan=lifespan)

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
    import sys
    import os
    
    # Ensure the project root is in sys.path and PYTHONPATH 
    # so uvicorn subprocesses can correctly resolve "backend.main:app"
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    
    current_pythonpath = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = f"{root_dir}{os.pathsep}{current_pythonpath}" if current_pythonpath else root_dir

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
