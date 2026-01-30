from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app, get_session
from app.models import Profile

# Setup in-memory DB for testing (so we don't break the real DB)
engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

def create_test_db():
    SQLModel.metadata.create_all(engine)
    # Seed a dummy profile
    with Session(engine) as session:
        profile = Profile(
            name="Test User",
            email="test@test.com",
            role="Tester",
            bio="Testing",
            github="http://github.com",
            linkedin="http://linkedin.com"
        )
        session.add(profile)
        session.commit()

def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Service is healthy"}

def test_read_profile():
    create_test_db() # Ensure DB is ready
    response = client.get("/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@test.com"