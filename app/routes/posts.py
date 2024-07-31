from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_farpost_repository
from app.repositories import FarpostRepository
from app.schemes.farpost import PostPreview, Post


route = APIRouter(prefix="/post", tags=["Farpost posts"])


@route.get("", response_model=list[Post])
async def show_posts(
        repository: FarpostRepository = Depends(get_farpost_repository)
) -> list[Post]:
    posts = await repository.list("Системы+видеонаблюдения")
    return posts


@route.get("/{post_id}", response_model=Post)
async def get_post(
    post_id: int, 
    repository: FarpostRepository = Depends(get_farpost_repository)
) -> Post:
    post = await repository.get(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post
