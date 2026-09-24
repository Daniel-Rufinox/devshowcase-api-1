from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Profile
from ..schemas import ProfileCreate, ProfileResponse
from ..repositories.profile_repository import ProfileRepository


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
    repository = ProfileRepository(db)

    existing_profile = repository.get_by_email(
        profile_data.email
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

    return repository.create(profile)


@router.get(
    "/{profile_id}",
    response_model=ProfileResponse
)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    repository = ProfileRepository(db)

    profile = repository.get_by_id(profile_id)

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Perfil não encontrado."
        )

    return profile