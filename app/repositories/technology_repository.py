from sqlalchemy.orm import Session

from ..models import Technology


class TechnologyRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, technology_id: int):
        return (
            self.db.query(Technology)
            .filter(Technology.id == technology_id)
            .first()
        )

    def get_by_name(self, name: str):
        return (
            self.db.query(Technology)
            .filter(Technology.name == name)
            .first()
        )

    def get_by_ids(self, technology_ids: list[int]):
        return (
            self.db.query(Technology)
            .filter(Technology.id.in_(technology_ids))
            .all()
        )

    def list_all(self):
        return self.db.query(Technology).all()

    def create(self, technology: Technology):
        self.db.add(technology)
        self.db.commit()
        self.db.refresh(technology)

        return technology