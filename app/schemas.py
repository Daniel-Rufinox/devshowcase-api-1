from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


# =========================
# PROFILE
# =========================

class ProfileCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    bio: str | None = Field(default=None, max_length=1000)
    github_url: HttpUrl | None = None
    linkedin_url: HttpUrl | None = None


class ProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    bio: str | None
    github_url: HttpUrl | None
    linkedin_url: HttpUrl | None

    model_config = ConfigDict(from_attributes=True)


# =========================
# TECHNOLOGY
# =========================

class TechnologyCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class TechnologyResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# FEEDBACK
# =========================

class FeedbackCreate(BaseModel):
    author: str = Field(..., min_length=2, max_length=100)
    comment: str = Field(..., min_length=2, max_length=1000)
    rating: int = Field(..., ge=1, le=5)


class FeedbackResponse(BaseModel):
    id: int
    author: str
    comment: str
    rating: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# PROJECT
# =========================

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=150)
    description: str = Field(..., min_length=5, max_length=2000)
    repository_url: HttpUrl
    deploy_url: HttpUrl | None = None
    profile_id: int = Field(..., gt=0)
    technology_ids: list[int] = Field(default_factory=list)


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    repository_url: HttpUrl
    deploy_url: HttpUrl | None
    profile_id: int
    technology_ids: list[int]
    average_rating: float
    upvotes: int

    model_config = ConfigDict(from_attributes=True)