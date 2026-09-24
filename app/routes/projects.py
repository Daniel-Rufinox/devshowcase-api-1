from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Project
from ..schemas import (
    FeedbackCreate,
    FeedbackResponse,
    ProjectCreate,
    ProjectResponse
)
from ..repositories.profile_repository import ProfileRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.technology_repository import TechnologyRepository
from ..services.project_service import ProjectService


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)


def project_to_response(project: Project):
    return ProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        repository_url=project.repository_url,
        deploy_url=project.deploy_url,
        profile_id=project.profile_id,
        technology_ids=[
            technology.id
            for technology in project.technologies
        ],
        average_rating=project.average_rating,
        upvotes=project.upvotes
    )


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    profile_repository = ProfileRepository(db)
    technology_repository = TechnologyRepository(db)
    project_repository = ProjectRepository(db)

    profile = profile_repository.get_by_id(
        project_data.profile_id
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Perfil não encontrado."
        )

    technologies = []

    if project_data.technology_ids:
        technologies = technology_repository.get_by_ids(
            project_data.technology_ids
        )

        if len(technologies) != len(
            set(project_data.technology_ids)
        ):
            raise HTTPException(
                status_code=400,
                detail="Uma ou mais tecnologias não existem."
            )

    project = Project(
        title=project_data.title,
        description=project_data.description,
        repository_url=str(project_data.repository_url),
        deploy_url=str(project_data.deploy_url)
        if project_data.deploy_url else None,
        profile_id=project_data.profile_id,
        technologies=technologies
    )

    project = project_repository.create(project)

    return project_to_response(project)


@router.get(
    "",
    response_model=list[ProjectResponse]
)
def list_projects(
    technology: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Project)

    if technology:
        query = query.filter(
            Project.technologies.any(name=technology)
        )

    projects = (
        query
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return [
        project_to_response(project)
        for project in projects
    ]


@router.post(
    "/{project_id}/feedbacks",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED
)
def create_feedback(
    project_id: int,
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db)
):
    service = ProjectService(db)

    return service.add_feedback(
        project_id,
        feedback_data
    )


@router.put(
    "/{project_id}/upvote",
    response_model=ProjectResponse
)
def upvote_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    service = ProjectService(db)

    project = service.upvote_project(project_id)

    return project_to_response(project)