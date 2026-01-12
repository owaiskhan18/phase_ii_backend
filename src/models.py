from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel, Session

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    password_hash: str = Field(nullable=False)

    tasks: List["Task"] = Relationship(back_populates="owner")

class Task(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(nullable=False)
    is_completed: bool = Field(default=False, nullable=False)
    
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    owner: User = Relationship(back_populates="tasks")
