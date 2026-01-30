from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, col
from typing import List, Optional

from .database import create_db_and_tables, get_session
from .models import Project, Skill, Profile

app = FastAPI(title="Me-API Playground")

# CORS (Requirement: Must call hosted API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 1. Health Check (Acceptance Criteria)
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Service is healthy"}

# 2. Profile Endpoints
@app.get("/profile", response_model=Profile)
def get_profile(session: Session = Depends(get_session)):
    profile = session.exec(select(Profile)).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not seeded")
    return profile

# 3. Projects & Search (Supports ?skill=python and ?q=term)
@app.get("/projects", response_model=List[Project])
def get_projects(
    skill: Optional[str] = None, 
    q: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Project)
    
    if skill:
        # Filter where tags contain the skill (case insensitive)
        query = query.where(col(Project.tags).contains(skill.lower()))
    
    if q:
        # Search in title or description
        query = query.where(
            col(Project.title).contains(q) | col(Project.description).contains(q)
        )
        
    return session.exec(query).all()

@app.get("/skills", response_model=List[Skill])
def get_skills(session: Session = Depends(get_session)):
    return session.exec(select(Skill)).all()

# Serve Frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")