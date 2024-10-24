from typing import Optional

from pydantic import BaseModel

class Comment(BaseModel):
    comment_id: Optional[int] = None
    author: str
    content: str
    article_id: Optional[int] = None
