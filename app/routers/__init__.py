from fastapi import APIRouter
from . import user, material, fit_up, final, ndt

# Create a main router
def get_routers():
    main_router = APIRouter()

    # Include all routers in the main router
    main_router.include_router(user.router, prefix="/users", tags=["users"])
    main_router.include_router(material.router, prefix="/materials", tags=["materials"])
    main_router.include_router(fit_up.router, prefix="/fit-ups", tags=["fit-ups"])
    main_router.include_router(final.router, prefix="/finals", tags=["finals"])
    main_router.include_router(ndt.router, prefix="/ndts", tags=["ndts"])

    return main_router
