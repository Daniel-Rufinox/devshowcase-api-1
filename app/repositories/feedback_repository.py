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

    def calculate_average_rating(self, project_id: int):
        feedbacks = self.list_by_project(project_id)

        if not feedbacks:
            return 0.0

        total = sum(
            feedback.rating
            for feedback in feedbacks
        )

        return round(total / len(feedbacks), 2)