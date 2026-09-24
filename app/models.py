from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, Float
from sqlalchemy.orm import relationship

from .database import Base


# Relacionamento N:N entre Project e Technology
project_technology = Table(
    "project_technology",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("technology_id", ForeignKey("technologies.id"), primary_key=True)
)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    bio = Column(Text, nullable=True)
    github_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)

    projects = relationship(
        "Project",
        back_populates="profile",
        cascade="all, delete-orphan"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    repository_url = Column(String(255), nullable=False)
    deploy_url = Column(String(255), nullable=True)

    # Campos da segunda etapa
    average_rating = Column(Float, nullable=False, default=0.0)
    upvotes = Column(Integer, nullable=False, default=0)

    profile_id = Column(
        Integer,
        ForeignKey("profiles.id"),
        nullable=False
    )

    profile = relationship(
        "Profile",
        back_populates="projects"
    )

    technologies = relationship(
        "Technology",
        secondary=project_technology,
        back_populates="projects"
    )

    feedbacks = relationship(
        "Feedback",
        back_populates="project",
        cascade="all, delete-orphan"
    )


class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    projects = relationship(
        "Project",
        secondary=project_technology,
        back_populates="technologies"
    )


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String(100), nullable=False)
    comment = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    project = relationship(
        "Project",
        back_populates="feedbacks"
    )