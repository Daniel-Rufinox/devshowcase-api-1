from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Profile
from ..schemas import ProfileCreate, ProfileResponse

router = APIRouter(
    prefix="/api/profiles",
    tags=["Profiles"]
)


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED
)
def create_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db)
):
    existing_profile = (
        db.query(Profile)
        .filter(Profile.email == profile_data.email)
        .first()
    )

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado."
        )

    profile = Profile(
        name=profile_data.name,
        email=profile_data.email,
        bio=profile_data.bio,
        github_url=str(profile_data.github_url)
        if profile_data.github_url else None,
        linkedin_url=str(profile_data.linkedin_url)
        if profile_data.linkedin_url else None
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get(
    "/{profile_id}",
    response_model=ProfileResponse
)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    profile = (
        db.query(Profile)
        .filter(Profile.id == profile_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Perfil não encontrado."
        )

    return profile