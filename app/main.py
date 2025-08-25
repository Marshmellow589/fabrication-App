from fastapi import FastAPI
from .database import SessionLocal, engine
from . import models, schemas, routers

app = FastAPI()

# Create all tables in the database
@app.on_event("startup")
def create_tables():
    models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(routers.user.router)
app.include_router(routers.material.router)
app.include_router(routers.fit_up.router)
app.include_router(routers.final.router)
app.include_router(routers.ndt.router)
