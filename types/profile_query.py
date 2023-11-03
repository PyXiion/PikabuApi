from typing import TypedDict, Optional

class ProfileQuery(TypedDict):
  user_name: str

  user_id: Optional[int]