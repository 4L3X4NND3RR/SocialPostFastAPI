from typing import Optional
from pydantic import BaseModel


class SocialPost(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: Optional[bool] = True
