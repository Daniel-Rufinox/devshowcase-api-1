from sqlalchemy.orm import Session

from ..models import Profile


class ProfileRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, profile_id: int):
        return (
            self.db.query(Profile)
            .filter(Profile.id == profile_id)
            .first()
        )

    def get_by_email(self, email: str):
        return (
            self.db.query(Profile)
            .filter(Profile.email == email)
            .first()
        )

    def create(self, profile: Profile):
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile