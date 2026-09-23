from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Profile, Project, Technology
from ..schemas import ProjectCreate, ProjectResponse

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
    profile = (
        db.query(Profile)
        .filter(Profile.id == project_data.profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Perfil não encontrado."
        )

    technologies = []

    if project_data.technology_ids:
        technologies = (
            db.query(Technology)
            .filter(
                Technology.id.in_(project_data.technology_ids)
            )
            .all()
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

    db.add(project)
    db.commit()
    db.refresh(project)

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
    projects = db.query(Project).all()

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