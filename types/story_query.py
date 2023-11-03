from typing import TypedDict, Optional

class StoryQuery(TypedDict):
  story_id: int
  page: Optional[int]
  
  user_id: Optional[int]