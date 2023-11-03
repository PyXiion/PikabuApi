from typing import TypedDict, List, Optional

class CreateCommentQuery(TypedDict):
  story_id: int
  user_id: int
  desc: str
  plain_text: Optional[bool]
  parent_id: Optional[int]
  images: Optional[List[str]]