from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Feedback
from ..repositories.feedback_repository import FeedbackRepository
from ..repositories.project_repository import ProjectRepository
from ..schemas import FeedbackCreate


class ProjectService:

    def __init__(self, db: Session):
        self.db = db
        self.project_repository = ProjectRepository(db)
        self.feedback_repository = FeedbackRepository(db)

    def add_feedback(
        self,
        project_id: int,
        feedback_data: FeedbackCreate
    ):
        project = self.project_repository.get_by_id(project_id)

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Projeto não encontrado."
            )

        feedback = Feedback(
            author=feedback_data.author,
            comment=feedback_data.comment,
            rating=feedback_data.rating,
            project_id=project_id
        )

        feedback = self.feedback_repository.create(feedback)

        project.average_rating = (
            self.feedback_repository.calculate_average_rating(
                project_id
            )
        )

        self.db.commit()
        self.db.refresh(project)

        return feedback

    def upvote_project(self, project_id: int):
        project = self.project_repository.get_by_id(project_id)

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Projeto não encontrado."
            )

        project.upvotes += 1

        self.db.commit()
        self.db.refresh(project)

        return project