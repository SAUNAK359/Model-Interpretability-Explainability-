from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

# Shared properties
class ProjectBase(SQLModel):
    title: str
    description: str
    link: Optional[str] = None
    tags: str  # Comma-separated tags for easier filtering (e.g. "python,react")

class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: str # e.g., "Backend", "Frontend"

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    role: str
    bio: str
    github: str
    linkedin: str