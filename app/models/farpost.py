from sqlalchemy.ext.hybrid import hybrid_method
import sqlalchemy as sa

from .base import Base
from app import schemes


class PostPreview(Base):
    __tablename__ = "farposts_preview"
    
    id = sa.Column(sa.BigInteger(), primary_key=True)
    title = sa.Column(sa.String(70))
    query = sa.Column(sa.Text())
    author = sa.Column(sa.String(64))
    views_count = sa.Column(sa.Integer())
    position = sa.Column(sa.Integer())

    @hybrid_method
    def to_scheme(self) -> schemes.farpost.PostPreview:
        return schemes.farpost.PostPreview(
            id=self.id,
            title=self.title,
            query=self.query,
            author=self.author,
            views_count=self.views_count,
            position=self.position
        )
