from typing import TypedDict, Optional

class CommunityQuery(TypedDict):
  name: str

  user_id: Optional[int]