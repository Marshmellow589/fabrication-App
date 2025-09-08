from .base import CRUDBase
from .user import user as user_crud
from .project import project as project_crud
from .material import material as material_crud
from .fitup import fitup as fitup_crud
from .final_inspection import final_inspection as final_inspection_crud
from .ndt_request import ndt_request as ndt_request_crud

__all__ = [
    "CRUDBase",
    "user_crud",
    "project_crud",
    "material_crud",
    "fitup_crud",
    "final_inspection_crud",
    "ndt_request_crud"
]
