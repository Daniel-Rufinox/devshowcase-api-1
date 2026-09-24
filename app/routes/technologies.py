from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Technology
from ..schemas import TechnologyCreate, TechnologyResponse
from ..repositories.technology_repository import TechnologyRepository


router = APIRouter(
    prefix="/api/technologies",
    tags=["Technologies"]
)


@router.post(
    "",
    response_model=TechnologyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_technology(
    technology_data: TechnologyCreate,
    db: Session = Depends(get_db)
):
    repository = TechnologyRepository(db)

    existing_technology = repository.get_by_name(
        technology_data.name
    )

    if existing_technology:
        raise HTTPException(
            status_code=400,
            detail="Tecnologia já cadastrada."
        )

    technology = Technology(
        name=technology_data.name
    )

    return repository.create(technology)


@router.get(
    "",
    response_model=list[TechnologyResponse]
)
def list_technologies(
    db: Session = Depends(get_db)
):
    repository = TechnologyRepository(db)

    return repository.list_all()