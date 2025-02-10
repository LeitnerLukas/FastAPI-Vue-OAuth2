from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import user, auth, test, activities, classes, parent_infos
from database.config import engine, database, Base


app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(activities.router)
app.include_router(classes.router)
app.include_router(parent_infos.router)
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


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
