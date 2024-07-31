from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete

from app import models, schemes


class FarpostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = models.farpost.PostPreview
    
    async def get(self, id: str) -> schemes.farpost.PostPreview | None:
        item = await self.session.get(self.model, id)
        if item is not None:
            item = item.to_scheme()
        return item
    
    async def list(self, query: str, limit: int = 10, offset: int = 0) -> list[schemes.farpost.PostPreview]:
        statement = select(models.PostPreview).where(
            models.PostPreview.query == query
        ).order_by(
            models.PostPreview.position
        ).limit(limit).offset(offset)
        query = await self.session.execute(statement)
        return [post[0].to_scheme() for post in query.all()]
    
    async def create(self, data: schemes.farpost.PostPreview) -> int:
        item = self.model(**data.model_dump())
        self.session.add(item)
        await self.session.commit()
        return item.id
        
    async def delete(self, post: schemes.farpost.PostPreview) -> bool:
        statement = delete(models.PostPreview).where(models.PostPreview.id == post.id)
        await self.session.execute(statement)
        await self.session.commit()
        
        item = await self.get(post.id)
        return item is None
