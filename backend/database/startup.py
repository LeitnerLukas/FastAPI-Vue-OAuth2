from crud.roles import RolesCRUD
import schemas.roles as roles_schema
from database.config import async_session, engine, Base, database

async def initialize_database():
    await database.connect()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        db = RolesCRUD(session)
        existing_roles = await db.get_roles()
        
        if not existing_roles:
            roles = [
                roles_schema.Create(
                    name="superuser",
                    approvement_permission=False,
                    super_approvement_permission=False,
                    request_permission=False,
                    change_permission=True
                ),
                roles_schema.Create(
                    name="department_head",
                    approvement_permission=True,
                    super_approvement_permission=False,
                    request_permission=True,
                    change_permission=False
                ),
                roles_schema.Create(
                    name="director",
                    approvement_permission=True,
                    super_approvement_permission=True,
                    request_permission=True,
                    change_permission=False
                ),
                roles_schema.Create(
                    name="teacher",
                    approvement_permission=False,
                    super_approvement_permission=False,
                    request_permission=True,
                    change_permission=False
                ),
            ]

            for role in roles:
                await db.create_role(role)

            await session.commit()