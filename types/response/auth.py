from typing import TypedDict

class Auth(TypedDict):
  user_id: int
  user_name: str
  avatar: str
  rating: float
  subscribers_count: int
  remember: str

  is_add_comment_photo_ban: bool
  min_rating_to_add_comment_photo: int