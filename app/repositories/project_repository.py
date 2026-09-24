from sqlalchemy.orm import Session

from ..models import Project


class ProjectRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, project_id: int):
        return (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

    def list_all(self):
        return self.db.query(Project).all()

    def create(self, project: Project):
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project