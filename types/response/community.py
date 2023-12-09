from typing import TypedDict, List
from .user_ref import UserRef

class GetCommunity(TypedDict):
  id: int
  link_name: str

  name: str
  description: str
  rules: str
  restriction: str

  community_admin: UserRef
  community_moderators: List[UserRef]
  community_chiefs: List[UserRef]

  url: str
  avatar_url: str
  bg_image_url: str

  tags: List[str]

  is_locked: str
  is_nsfw: str
  lock_message: None

  stories: int
  subscribers: int

  # user info
  is_ignored: bool
  is_subscribed: bool
  is_in_preview_mode: bool