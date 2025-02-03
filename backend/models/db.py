from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Table, ForeignKey, Enum
from sqlalchemy.orm import relationship
from crud.types import AcceptState

from database.config import Base

user_activity = Table(
    "user_activity",
    Base.metadata,
    Column("username", ForeignKey("users.username"), primary_key=True),
    Column("activity_id", ForeignKey("activities.activity_id"), primary_key=True),
    Column("is_leader", Boolean, default=False)
)

class_activity = Table(
    "class_activity",
    Base.metadata,
    Column("class_id", ForeignKey("classes.class_id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.activity_id"), primary_key=True),
    Column("girl_count", Integer),
    Column("boy_count", Integer)
)

user_role = Table(
    "user_role",
    Base.metadata,
    Column("username", ForeignKey("users.username"), primary_key=True),
    Column("role_name", ForeignKey("roles.name"), primary_key=True)
)

# Create User class
class UserModels(Base):
    __tablename__ = "users"
    username = Column(String, unique=True, primary_key=True)
    name = Column(String)
    create_time = Column(DateTime, default=datetime.now())
    last_login = Column(DateTime, default=datetime.now())

    roles = relationship("Roles", secondary=user_role, back_populates="users")
    activities = relationship("Activities", secondary=user_activity, back_populates="users")

    def __init__(self, username: str, name: str):
        self.username = username
        self.name = name


    def __repr__(self) -> str:
        return f"<UserModels(username={self.username}, name={self.name}, roleId={self.roleId})>"

class Roles(Base):
    __tablename__ = "roles"
    name = Column(String, unique=True, primary_key=True)
    approvement_permission = Column(Boolean)
    super_approvement_permission = Column(Boolean)
    request_permission = Column(Boolean)
    change_permission = Column(Boolean)

    users = relationship("UserModels", secondary=user_role, back_populates="roles")

    def __init__(self, name: str, approvement_permission: bool, super_approvement_permission: bool, request_permission: bool, change_permission: bool):
        self.name = name
        self.approvement_permission = approvement_permission
        self.super_approvement_permission = super_approvement_permission
        self.request_permission = request_permission
        self.change_permission = change_permission
    
    def __repr__(self) -> str:
        return f"<Roles(name={self.name}, approvement_permission={self.approvement_permission}, super_approvement_permission={self.super_approvement_permission}, request_permission={self.request_permission}, change_permission={self.change_permission})>"
    

class Activities(Base):
    __tablename__ = "activities"
    activity_id = Column(Integer, primary_key=True, autoincrement=True)

    location = Column(String)
    description = Column(String)
    curriculum_reference = Column(String)

    cost = Column(Integer)
    transfer_cost = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    sga_approved = Column(Boolean, default=False)
    state = Column(Enum(AcceptState), default=AcceptState.REQUESTED)

    create_time = Column(DateTime, default=datetime.now())
    last_update = Column(DateTime, default=datetime.now())

    users = relationship("UserModels", secondary=user_activity, back_populates="activities")
    classes = relationship("Classes", secondary=class_activity, back_populates="activities")
    parent_infos = relationship("ParentInfos", back_populates="activity")

    def __repr__(self) -> str:
        return f"<Activities(location={self.location}, description={self.description}, curriculum_reference={self.curriculum_reference}, cost={self.cost}, transfer_cost={self.transfer_cost}, start_time={self.start_time}, end_time={self.end_time})>"
    

class Classes(Base):
    __tablename__ = "classes"
    class_id = Column(String, primary_key=True)
    girl_count = Column(Integer)
    boy_count = Column(Integer)

    activities = relationship("Activities", secondary=class_activity, back_populates="classes")

    def __repr__(self) -> str:
        return f"<Classes(girl_count={self.girl_count}, boy_count={self.boy_count})>"

class ParentInfos(Base):
    __tablename__ = "parent_infos"
    parent_info_id = Column(Integer, primary_key=True, autoincrement=True)
    activity_id = Column(Integer, ForeignKey("activities.activity_id"))
    text = Column(String)

    activity = relationship("Activities", back_populates="parent_infos")

    def __init__(self, text: str, activity_id: int):
        self.text = text
        self.activity_id = activity_id
    
