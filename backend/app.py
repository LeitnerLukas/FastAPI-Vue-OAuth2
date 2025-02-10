from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crud.dependencies import get_roles_crud
from crud.roles import RolesCRUD
import schemas.roles as roles_schema

from api import user, auth, test
from database.config import engine, database, Base


app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router, prefix="/api")
app.include_router(test.router)


methods = [
    "DELETE",
    "GET",
    "POST",
    "PUT",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173", "https://localhost:8008"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    superuser = roles_schema.Create(
        name="superuser",
        approvement_permission=False,
        super_approvement_permission=False,
        request_permission=False,
        change_permission=True
    )
    department_head = roles_schema.Create(
        name="department_head",
        approvement_permission=True,
        super_approvement_permission=False,
        request_permission=True,
        change_permission=False
    )
    director = roles_schema.Create(
        name="director",
        approvement_permission=True,
        super_approvement_permission=True,
        request_permission=True,
        change_permission=False
    )
    teacher = roles_schema.Create(
        name="teacher",
        approvement_permission=False,
        super_approvement_permission=False,
        request_permission=True,
        change_permission=False
    )

    db:RolesCRUD = get_roles_crud()
    await db.create_role(superuser)
    await db.create_role(department_head)
    await db.create_role(director)
    await db.create_role(teacher)
    


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
