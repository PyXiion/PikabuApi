from typing import TypedDict, List

class CommentDescription(TypedDict):
  images: List[str]
  text: str
  videos: List[str]

class Comment(TypedDict):
  # data for user
  can_block_author: bool
  can_edit: bool
  can_hide: bool
  can_ignore: bool
  can_replay: bool
  can_reveal: bool
  can_vote: bool
  curr_user_vote: int
  has_user_note: bool
  ignore_code: int
  ignored_by: List
  is_author_subscriber: bool
  is_comment_author: bool
  is_comment_saved: bool
  is_curr_user_community_moderator: bool
  is_curr_user_pikabu_team: bool
  is_current_user_sponsor: bool
  is_current_user_subscriber: bool
  is_ignored_user: bool
  is_unreaded: bool
  is_user_ignored: bool

  # Ids
  parent_id: int
  comment_id: int

  # Story data
  story_id: int
  story_subs_code: int
  story_title: str
  story_url: str
  story_user_id: int

  # Author info
  user_id: int
  user_name: str
  user_achievements_level: int
  user_approve: str
  user_avatar_url: str
  user_gender: str
  user_profile_deleted: bool
  user_profile_url: str

  # Comment content
  comment_desc: CommentDescription

  is_story_comment: bool
  comstory_data: None # ?

  # Rating and etc
  comment_minuses: int
  comment_pluses: int
  comment_rating: int
  comment_platform: None # ?
  comment_time: int

  # Flags
  is_community_subscriber: bool
  is_community_trusted_user: bool
  is_comstory: bool # is story answer
  is_deleted: bool
  is_hidden: bool
  is_hidden_comment: bool
  is_moderator_username: bool
  is_official: bool
  is_own_story: bool
  is_user_community_moderator: bool
  is_user_pikabu_team: bool