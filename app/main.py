from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import engine
from . import models, schemas, routers
import os

app = FastAPI()

# Create all tables in the database
@app.on_event("startup")
def create_tables():
    models.Base.metadata.create_all(bind=engine)

# Serve frontend static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the main frontend HTML file
@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")

# Include routers
app.include_router(routers.auth.router)
app.include_router(routers.user.router)
app.include_router(routers.material.router)
app.include_router(routers.fit_up.router)
app.include_router(routers.final.router)
app.include_router(routers.ndt.router)
