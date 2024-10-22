from typing import Optional

from pydantic import BaseModel

class Article(BaseModel):
    article_id: Optional[int] = None
    title: str
    slug: str
    content: str
    author: str