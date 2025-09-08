from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import auth, user, projects, material, fitup, final, ndt
from backend.app.database import engine, Base
import logging

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Industrial Inspection Platform API",
    description="检验数据管理平台API",
    version="1.0.0"
)
app.include_router(projects.router)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(material.router, prefix="/material", tags=["Material Inspection"])
app.include_router(fitup.router, prefix="/fitup", tags=["Fitup Inspection"])
app.include_router(final.router, prefix="/final", tags=["Final Inspection"])
app.include_router(ndt.router, prefix="/ndt", tags=["NDT Requests"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Industrial Inspection Platform API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
