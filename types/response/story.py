from typing import TypedDict, List

class Story(TypedDict):
  # story info
  story_id: int
  story_time: int
  story_title: str
  story_url: str

  parent_story_id: None | str

  story_data: List[any]

  # Tags
  tags: List[str]

  # Flags
  is_adult: bool
  is_authors: bool
  is_longpost: bool
  is_unique_author_story: bool
  is_deleted: bool
  is_comm_disabled: bool
  is_hot_comments: bool

  has_author_comments: bool
  can_donate: bool

  # Statistic
  story_pluses: int | None
  story_minuses: int | None
  story_digs: int | None
  comments_count: int

  # Community info
  community_id: int
  community_name: str
  community_is_nsfw: bool
  community_link: str

  # Author info
  user_id: int
  user_name: str
  user_profile_url: str