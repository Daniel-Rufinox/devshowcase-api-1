from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Profile, Project
from ..schemas import ProjectCreate, ProjectResponse
from ..repositories.profile_repository import ProfileRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.technology_repository import TechnologyRepository


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
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

    project_repository.create(project)

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
        ]
    )


@router.get(
    "",
    response_model=list[ProjectResponse]
)
def list_projects(
    db: Session = Depends(get_db)
):
    repository = ProjectRepository(db)

    projects = repository.list_all()

    return [
        ProjectResponse(
            id=project.id,
            title=project.title,
            description=project.description,
            repository_url=project.repository_url,
            deploy_url=project.deploy_url,
            profile_id=project.profile_id,
            technology_ids=[
                technology.id
                for technology in project.technologies
            ]
        )
        for project in projects
    ]