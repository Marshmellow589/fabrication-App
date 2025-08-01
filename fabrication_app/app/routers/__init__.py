from .material import router as material_router
from .fit_up import router as fit_up_router
from .final import router as final_router
from .ndt import router as ndt_router
from .auth import router as auth_router

__all__ = ["material_router", "fit_up_router", "final_router", "ndt_router", "auth_router"]
