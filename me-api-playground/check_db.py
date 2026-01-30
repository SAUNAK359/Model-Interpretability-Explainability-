from sqlmodel import Session, select
from app.database import engine
from app.models import Profile, Project, Skill

def check():
    with Session(engine) as session:
        profiles = session.exec(select(Profile)).all()
        projects = session.exec(select(Project)).all()
        skills = session.exec(select(Skill)).all()
        print(f"Profiles: {len(profiles)}")
        for p in profiles:
            print(f" - {p.name} ({p.role})")
        
        print(f"Projects: {len(projects)}")
        for p in projects:
            print(f" - {p.title} (Tags: {p.tags})")

        print(f"Skills: {len(skills)}")

if __name__ == "__main__":
    try:
        check()
    except Exception as e:
        print(f"Error: {e}")
