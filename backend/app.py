from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from crud.roles import RolesCRUD
import schemas.roles as roles_schema
from database.config import async_session
from api import user, auth, test, roles, activities, classes, parent_infos
from database.config import engine, database, Base
from database.startup import initialize_database

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(activities.router)
app.include_router(classes.router)
app.include_router(parent_infos.router)
app.include_router(test.router)
app.include_router(roles.router)

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
    await initialize_database()  # Call the new function

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()