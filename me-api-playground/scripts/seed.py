import sys
import os

# Add the parent directory to sys.path to find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.database import engine, create_db_and_tables
from app.models import Profile, Project, Skill

def seed_data():
    print("Seeding database...")
    create_db_and_tables()
    
    with Session(engine) as session:
        # 1. Check if data exists to prevent duplicates
        if session.exec(select(Profile)).first():
            print("Data already seeded. Skipping.")
            return

        # 2. Create Profile
        # NOTE: I updated this based on your GitHub handle. 
        # PLEASE UPDATE 'Your Real Name' and 'your@email.com' before running!
        my_profile = Profile(
            name="Saunak",  # Update this!
            email="saunak@example.com", # Update this!
            role="AI & Full Stack Engineer",
            bio="Building intelligent systems with LLMs, RAG, and scalable Backend architectures.",
            github="https://github.com/SAUNAK359",
            linkedin="https://linkedin.com/in/saunak" # Update if needed
        )
        session.add(my_profile)

        # 3. Add Skills
        skills = [
            Skill(name="Python", category="Backend"),
            Skill(name="FastAPI", category="Backend"),
            Skill(name="LLM/RAG", category="AI"),
            Skill(name="Vector DBs", category="AI"),
            Skill(name="React", category="Frontend"),
            Skill(name="Kubernetes", category="DevOps"),
        ]
        session.add_all(skills)

        # 4. Add Projects (Fixed Indentation)
        projects = [
            Project(
                title="Analytics@LLM",
                description=(
                    "Enterprise-grade, agentic analytics platform enabling conversational, "
                    "LLM-driven dashboard generation with dynamic MCP-based visualization, "
                    "multi-modal data ingestion, governance-aware reasoning, and cloud-native deployment."
                ),
                tags="python, llm, agentic-ai, analytics, streamlit, fastapi, vector-db, kubernetes, data-engineering",
                link="https://github.com/SAUNAK359/GreedyAnalytics"
            ),
            Project(
                title="Fortune Retrieval",
                description=(
                    "Intelligent information retrieval system leveraging vector search and "
                    "semantic ranking to provide context-aware answers over large document corpora."
                ),
                tags="python, nlp, vector-search, faiss, rag, information-retrieval",
                link="https://github.com/SAUNAK359/fortune-retrieval"
            ),
            Project(
                title="InstaML",
                description=(
                    "Automated machine learning platform that streamlines data preprocessing, "
                    "model selection, training, evaluation, and deployment for rapid ML experimentation."
                ),
                tags="machine-learning, automl, python, scikit-learn, xgboost, mlops",
                link="https://github.com/SAUNAK359/InstaML"
            )
        ]
        session.add_all(projects)

        session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()