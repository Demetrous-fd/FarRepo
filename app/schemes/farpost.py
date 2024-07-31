from pydantic import BaseModel, Field


class Post(BaseModel):
    id: int = Field(...)
    title: str = Field(...)
    author: str | None = Field(None)
    views_count: int = Field(...)
    position: int = Field(...)


class PostPreview(Post):
    query: str = Field(...)
