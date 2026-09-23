from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Technology
from ..schemas import TechnologyCreate, TechnologyResponse

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
    existing_technology = (
        db.query(Technology)
        .filter(Technology.name == technology_data.name)
        .first()
    )

    if existing_technology:
        raise HTTPException(
            status_code=400,
            detail="Tecnologia já cadastrada."
        )

    technology = Technology(
        name=technology_data.name
    )

    db.add(technology)
    db.commit()
    db.refresh(technology)

    return technology


@router.get(
    "",
    response_model=list[TechnologyResponse]
)
def list_technologies(
    db: Session = Depends(get_db)
):
    return db.query(Technology).all()