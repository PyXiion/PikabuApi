from typing import TypedDict, List

class Award(TypedDict):
  id: str
  award_id: str
  user_id: str

  award_title: str
  award_image: str

  story_id: str
  story_title: str

  comment_id: str
  special_url: str
  link: str

  date: str
  is_hidden: str

class ProfileInner(TypedDict):
  # Main
  user_id: int
  user_name: str
  about: str
  gender: int

  registration_duration: str
  signup_date: int

  public_ban_history: list # ???
  user_ban_time: None # ???

  # Statistic
  rating: float

  subscribers_count: int
  comments_count: int
  stories_count: int
  stories_hot_count: int
  stories_queue_count: int
  pluses_count: int
  minuses_count: int

  cedit_changes_count: int
  cedit_votes_count: int

  # Flags
  is_rating_ban: bool
  is_user_banned: bool
  is_user_fully_banned: bool
  is_show_extended_profile: bool
  is_advert_blogs_user: bool
  header_bg_forbidden: bool

  is_slow_mode_enabled: bool
  slow_mode_text: str | None

  # Etc
  awards: List[Award]

  approved: str

class Profile(TypedDict):
  user: ProfileInner