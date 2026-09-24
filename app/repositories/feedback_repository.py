from sqlalchemy.orm import Session

from ..models import Feedback


class FeedbackRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, feedback_id: int):
        return (
            self.db.query(Feedback)
            .filter(Feedback.id == feedback_id)
            .first()
        )

    def list_by_project(self, project_id: int):
        return (
            self.db.query(Feedback)
            .filter(Feedback.project_id == project_id)
            .all()
        )

    def create(self, feedback: Feedback):
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)

        return feedback